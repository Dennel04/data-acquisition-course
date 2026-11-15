// DA2 measurement only. ADC setup/8-read average/JSON-lines/10 ms cadence
// follow Lab 1 sensor.cpp and comms.cpp. No pressure conversion or pump logic.
#include <Arduino.h>
#include <ArduinoJson.h>
#include <M5Unified.h>
#include <esp_log.h>
#include "sampling.h"

namespace {
constexpr int kAdcPin = 5;
char line[160]{}, config[6]{}, runId[17]{};
size_t used = 0;
acquisition::Mode mode = acquisition::Mode::Auto;
uint32_t lineStarted = 0, sequence = 0, displayAt = 0;
// Why a managed run ended without measure_stop; kept on the LCD until the next start.
const char* stopReason = nullptr;
// The ESP32-S3 core's USB 'connected' flag can drop for a moment while the host stays attached
// (15.11.26: reason usb_lost in 2 of 13 runs, no reconnect in Windows). Stop only if it stays down.
constexpr uint32_t kUsbLostMs = 100;
uint32_t usbDownSince = 0, usbFlickers = 0;
bool usbDown = false;
acquisition::Clock sampling;

void status(const char* state) {
  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.setCursor(2,2);
  M5.Display.setTextSize(1);
  M5.Display.setTextColor(TFT_WHITE, TFT_BLACK);
  M5.Display.println("DA2 MEASUREMENT");
  M5.Display.println(state);
  M5.Display.println("G5 / 12-bit / 11dB");
  M5.Display.println("not calibrated");
}
void stop() {
  mode = acquisition::Mode::Stopped;
  if (stopReason) {  // run had already ended on its own: report why, keep it on screen
    char reply[64];
    snprintf(reply,sizeof(reply),"{\"event\":\"stopped\",\"reason\":\"%s\"}",stopReason);
    Serial.println(reply);
    return;
  }
  Serial.println("{\"event\":\"stopped\"}");
  status("STOPPED");
}
void fail(const char* message) {
  mode = acquisition::Mode::Stopped;
  stopReason = message[0]=='\n' ? message+3 : message+2;  // text after "# "
  Serial.println(message);
  status(stopReason);
}
void command() {
  JsonDocument doc;
  if (deserializeJson(doc, line) != DeserializationError::Ok || !doc.is<JsonObject>()) {
    fail("# input_error"); return;
  }
  const char* cmd = doc["cmd"] | "";
  if (!std::strcmp(cmd,"measure_stop") && doc.size()==1 &&
      doc["cmd"].as<JsonString>().size()==12) { stop(); return; }
  const char* candidate = doc["config"] | "";
  const char* run = doc["run"] | "";
  if (mode == acquisition::Mode::Managed || std::strcmp(cmd,"measure_start") || doc.size()!=3 ||
      !acquisition::validConfig(candidate) || !acquisition::validRun(run) ||
      doc["config"].as<JsonString>().size()!=std::strlen(candidate) ||
      doc["run"].as<JsonString>().size()!=16 || doc["cmd"].as<JsonString>().size()!=13) {
    fail("# rejected_command"); return;
  }
  std::strcpy(config,candidate); std::strcpy(runId,run);
  mode = acquisition::Mode::Managed;  // no AUTO output after this command
  stopReason = nullptr;
  sequence=0;
  JsonDocument ack;
  ack["event"]="started"; ack["firmware"]="DA2_MEASURE_V1";
  ack["run"]=runId; ack["config"]=config;
  ack["period_ms"]=10; ack["adc_pin"]=5; ack["adc_bits"]=12;
  ack["adc_samples"]=8; ack["calibrated"]=false;
  serializeJson(ack,Serial); Serial.println();
  status(config);
  sampling.start(millis()); displayAt=millis()+250;
}
}  // namespace

void setup() {
  esp_log_level_set("*",ESP_LOG_NONE);
  auto cfg=M5.config(); M5.begin(cfg);
  M5.Display.setRotation(0); M5.Display.setBrightness(128);
  Serial.begin(115200); Serial.setTxTimeoutMs(50);  // 5 ms: core marked USB lost mid-run in ~1/4 of 10 s runs (15.11.26)
  pinMode(kAdcPin,INPUT);
  analogReadResolution(12);
  analogSetPinAttenuation(kAdcPin,ADC_11db);
  Serial.println("# DA2_MEASURE_V1;no_network;no_actuators;nvs_blocked");
  status("AUTO / config unknown");
  sampling.start(millis()); displayAt=millis();
}
void loop() {
  M5.update();
  if (used && millis()-lineStarted>1000) {
    used=0; fail("# partial_input_timeout");
  }
  // Bounded command intake; no arbitrary GPIO, actuator, or network command.
  for (int budget=0; budget<160 && Serial.available(); ++budget) {
    const int c=Serial.read();
    if (c=='\n') { line[used]=0; command(); used=0; }
    else if(c<32 || c>126 || used>=sizeof(line)-1) {
      used=0; fail("# framing_error"); break;
    } else { if(!used) lineStarted=millis(); line[used++]=static_cast<char>(c); }
  }
  if (!Serial) {
    if (!usbDown) { usbDown=true; usbDownSince=millis(); ++usbFlickers; }
    if (millis()-usbDownSince >= kUsbLostMs) {
      const auto previous=mode;
      mode=acquisition::afterDisconnect(mode);
      if (previous != mode) { stopReason = "usb_lost"; status("STOPPED / USB LOST"); }
    }
  } else {
    usbDown=false;
  }  // AUTO continues on LCD; reconnect never resumes a managed run
  if (mode == acquisition::Mode::Stopped) { delay(1); return; }
  const uint32_t now=millis();
  if (!sampling.due(now)) { delay(1); return; }
  const uint32_t measuredAt=millis();
  uint32_t sum=0;
  for(int i=0;i<8;++i) sum+=analogRead(kAdcPin);
  const int adc=sum/8;
  const bool refresh=static_cast<int32_t>(now-displayAt)>=0;
  if (mode == acquisition::Mode::Managed) {
  char packet[192];
  const int n=snprintf(packet,sizeof(packet),
      "{\"t\":%lu,\"adc\":%d,\"p\":null,\"pump\":null,\"config\":\"%s\",\"run\":\"%s\",\"seq\":%lu,\"missed\":%lu}\n",
      static_cast<unsigned long>(measuredAt),adc,config,runId,
      static_cast<unsigned long>(sequence++),static_cast<unsigned long>(sampling.missed));
  if(n<=0 || n>=static_cast<int>(sizeof(packet)) ||
      Serial.write(reinterpret_cast<const uint8_t*>(packet),n)!=static_cast<size_t>(n)) {
    fail("\n# serial_overrun"); return;
  }
  } else if (refresh && Serial) {
    // Human-readable preview, not a pressure reading or a logger sample.
    char preview[128];
    const int n=snprintf(preview,sizeof(preview),
        "# AUTO t_ms=%lu adc=%d config=unknown calibrated=false missed=%lu\n",
        static_cast<unsigned long>(measuredAt),adc,
        static_cast<unsigned long>(sampling.missed));
    // Never wait for a monitor; drop previews when its TX buffer is full.
    if (n>0 && n<static_cast<int>(sizeof(preview)) && Serial.availableForWrite()>=n)
      Serial.write(reinterpret_cast<const uint8_t*>(preview),n);
  }
  if(refresh) {
    displayAt=now+250;
    M5.Display.fillRect(0,65,128,22,TFT_BLACK);
    M5.Display.setCursor(2,65);
    M5.Display.printf("%s ADC %d\nUSB flicker %lu\n",
        mode == acquisition::Mode::Auto ? "AUTO" : config,adc,
        static_cast<unsigned long>(usbFlickers));
  }
}
