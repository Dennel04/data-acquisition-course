"""Run the actual firmware loop on the host with fake ADC, LCD and USB only."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

FIRMWARE=Path(__file__).resolve().parents[1]/"src/firmware"


class FirmwareAutoTests(unittest.TestCase):
    def test_actual_loop_and_commands_without_hardware(self):
        compiler=shutil.which("c++")
        self.assertIsNotNone(compiler)
        json_headers=FIRMWARE/".pio/libdeps/atoms3r/ArduinoJson/src"
        self.assertTrue((json_headers/"ArduinoJson.h").is_file(), "Run pio run -e atoms3r first")
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"Arduino.h").write_text(r'''
#pragma once
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
constexpr int INPUT=0, ADC_11db=3;
uint32_t tick=0;
int reads=0, configuredPin=-1, configuredBits=0, attenuation=-1;
uint32_t millis(){return tick;}
void delay(int ms){tick+=ms;}
void pinMode(int pin,int direction){assert(direction==INPUT);configuredPin=pin;}
void analogReadResolution(int n){configuredBits=n;}
void analogSetPinAttenuation(int pin,int db){assert(pin==5);attenuation=db;}
int analogRead(int pin){assert(pin==5);++reads;return 1234;}
struct Usb {
  bool connected=false, shortWrite=false;
  int capacity=256;
  std::string input, output;
  explicit operator bool() const {return connected;}
  void begin(int n){assert(n==115200);}
  void setTxTimeoutMs(int){}
  int available(){return input.size();}
  int read(){int c=static_cast<unsigned char>(input[0]);input.erase(0,1);return c;}
  int availableForWrite(){return capacity;}
  size_t write(const uint8_t* data,size_t n){
    if(shortWrite)return 0;
    output.append(reinterpret_cast<const char*>(data),n);return n;
  }
  size_t write(uint8_t byte){return write(&byte,1);}
  void println(const char* s=""){output+=s;output+='\n';}
} Serial;
''')
            (root/"M5Unified.h").write_text(r'''
#pragma once
#define TFT_BLACK 0
#define TFT_WHITE 1
struct Screen {
  std::string text;
  void fillScreen(int){text.clear();}
  void setCursor(int,int){}
  void setTextSize(int){}
  void setTextColor(int,int){}
  void setRotation(int){}
  void setBrightness(int){}
  void fillRect(int,int,int,int,int){}
  void println(const char* s){text+=s;text+='\n';}
  void printf(const char* format,const char* label,int adc){
    char buf[128];snprintf(buf,sizeof(buf),format,label,adc);text+=buf;
  }
};
struct Device {
  Screen Display;
  int config(){return 0;}
  void begin(int){}
  void update(){}
} M5;
''')
            (root/"esp_log.h").write_text("#define ESP_LOG_NONE 0\ninline void esp_log_level_set(const char*,int){}\n")
            (root/"test.cpp").write_text(r'''
#include "main.cpp"
const char* startRaw="{\"cmd\":\"measure_start\",\"config\":\"raw\",\"run\":\"0123456789abcdef\"}\n";
void send(const char* cmd){Serial.input=cmd;tick+=10;loop();}
int main(){
  setup();
  assert(configuredPin==5 && configuredBits==12 && attenuation==ADC_11db);
  assert(mode==acquisition::Mode::Auto);
  Serial.output.clear();
  for(int i=0;i<100;i++){tick=i*10;loop();}
  assert(reads==800); // 100 samples, eight readings each, without USB host
  assert(M5.Display.text.find("AUTO ADC 1234")!=std::string::npos);
  assert(Serial.output.empty());
  Serial.connected=true;tick=1000;loop();
  assert(Serial.output.find("# AUTO t_ms=1000 adc=1234 config=unknown calibrated=false missed=0")!=std::string::npos);
  Serial.capacity=0;Serial.output.clear();tick=1250;loop();
  assert(Serial.output.empty() && mode==acquisition::Mode::Auto);
  Serial.capacity=256;Serial.output.clear();send(startRaw);
  assert(mode==acquisition::Mode::Managed);
  assert(Serial.output.find("\"event\":\"started\"")!=std::string::npos);
  assert(Serial.output.find("\"seq\":0")!=std::string::npos);
  assert(Serial.output.find("\"p\":null,\"pump\":null")!=std::string::npos);
  assert(Serial.output.find("# AUTO")==std::string::npos);
  Serial.output.clear();tick+=10;loop();
  assert(Serial.output.find("\"seq\":1")!=std::string::npos);
  assert(Serial.output.find("# AUTO")==std::string::npos);
  Serial.output.clear();send("{\"cmd\":\"measure_stop\"}\n");
  assert(mode==acquisition::Mode::Stopped);
  assert(Serial.output=="{\"event\":\"stopped\"}\n");
  int before=reads;tick+=1000;loop();assert(reads==before);
  send(startRaw);Serial.connected=false;tick+=10;loop();
  assert(mode==acquisition::Mode::Stopped);
  Serial.connected=true;Serial.output.clear();tick+=1000;loop();
  assert(Serial.output.empty()); // no resume of a managed run on reconnect
  send(startRaw);Serial.shortWrite=true;tick+=10;loop();
  assert(mode==acquisition::Mode::Stopped);Serial.shortWrite=false;
  send(startRaw);send(startRaw);assert(mode==acquisition::Mode::Stopped);
  send("invalid\n");assert(mode==acquisition::Mode::Stopped);
  mode=acquisition::Mode::Auto;send("{\"cmd\":\"measure_stop\"}\n");
  assert(mode==acquisition::Mode::Stopped); // stop also suppresses AUTO
}
''')
            binary=root/"firmware_test"
            build=subprocess.run([compiler,"-std=c++11","-I",str(root),"-I",str(json_headers),
                                  "-I",str(FIRMWARE/"include"),"-I",str(FIRMWARE/"src"),
                                  str(root/"test.cpp"),"-o",str(binary)],capture_output=True,text=True)
            self.assertEqual(build.returncode,0,build.stderr)
            result=subprocess.run([str(binary)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)


if __name__=="__main__": unittest.main()
