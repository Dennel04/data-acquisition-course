// G5 meter: shows the G5 voltage and the MPX5700AP pressure on the LCD.
// Assumes G5 is wired straight to the sensor output (Lab 1 "raw" wiring).
// ADC settings, 3.70 V effective reference and transfer function come from
// data-acquisition/lab1/src/firmware/src/sensor.cpp. No pump, no Wi-Fi, no NVS.
// Press the screen to set the current pressure as zero for the "rel" line.
#include <Arduino.h>
#include <M5Unified.h>

constexpr int kAdcPin = 5;
constexpr float kAdcRef = 3.70f;      // Lab 1, measured 12.09.26
constexpr float kVcc = 5.0f;          // sensor supply, nominal
constexpr float kSlope = 0.0012858f;  // Vout = Vcc*(0.0012858*P + 0.04)
constexpr float kOffset = 0.04f;

float zeroKpa = NAN;

int readRaw() {
  long sum = 0;
  for (int i = 0; i < 8; ++i) sum += analogRead(kAdcPin);
  return sum / 8;
}

float smoothedKpa(float* voltsOut, int* rawOut) {
  // average 16 readings of 8 samples so the screen does not flicker
  long sum = 0;
  for (int i = 0; i < 16; ++i) { sum += readRaw(); delay(2); }
  int raw = sum / 16;
  float v = raw * (kAdcRef / 4095.0f);
  *voltsOut = v;
  *rawOut = raw;
  return (v / kVcc - kOffset) / kSlope;
}

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(kAdcPin, ADC_11db);
  M5.Display.setTextSize(1);
  M5.Display.fillScreen(TFT_BLACK);
  Serial.println("t_ms,adc_raw,g5_volts,p_abs_kpa,p_rel_kpa");
}

void loop() {
  M5.update();
  float v; int raw;
  float p = smoothedKpa(&v, &raw);
  if (isnan(zeroKpa) || M5.BtnA.wasPressed()) zeroKpa = p;
  float rel = p - zeroKpa;

  M5.Display.startWrite();
  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.setTextColor(TFT_DARKGREY);
  M5.Display.setFont(&fonts::Font0);
  M5.Display.setCursor(4, 4);   M5.Display.print("G5 METER (raw)");
  M5.Display.setTextColor(TFT_WHITE);
  M5.Display.setFont(&fonts::Font4);
  M5.Display.setCursor(4, 20);  M5.Display.printf("%.3f V", v);
  M5.Display.setTextColor(TFT_CYAN);
  M5.Display.setCursor(4, 52);  M5.Display.printf("%.1f kPa", p);
  M5.Display.setTextColor(TFT_YELLOW);
  M5.Display.setFont(&fonts::Font2);
  M5.Display.setCursor(4, 84);  M5.Display.printf("rel %+.1f kPa", rel);
  M5.Display.setTextColor(TFT_DARKGREY);
  M5.Display.setFont(&fonts::Font0);
  M5.Display.setCursor(4, 106); M5.Display.printf("raw %d  tap=zero", raw);
  M5.Display.setCursor(4, 116); M5.Display.print("not calibrated");
  M5.Display.endWrite();

  Serial.printf("%lu,%d,%.4f,%.2f,%.2f\n", millis(), raw, v, p, rel);
  delay(150);
}
