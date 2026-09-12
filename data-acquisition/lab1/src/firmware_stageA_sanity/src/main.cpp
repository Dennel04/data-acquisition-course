// Stage A -- sanity check only (README part 2, first paragraph):
// "Multimeter before connecting to Atom: 5V supply, Vout on atmosphere
//  ~0.85V. On Atom: read ADC -> print, so you can compare against the
//  multimeter reading before trusting anything downstream."
//
// This file deliberately does nothing else: no timing loop, no kPa
// conversion. Get raw counts + volts matching the multimeter first; the
// kPa math and the 10ms loop are Stage B/C (../firmware/).
//
// The on-screen status below is NOT part of that graded check -- it's
// just so you can tell at a glance the board booted and is still sampling
// (vs. frozen/crashed) without keeping the serial monitor open. The
// actual multimeter comparison is still done from the Serial CSV.

#include <Arduino.h>
#include <M5Unified.h>

constexpr int kAdcPin = 5;        // AtomS3(R) "G5" -- confirm against your
                                   // own wiring, not just this constant.

namespace {
uint32_t sampleCount = 0;
}

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg); // display init; also brings Serial up, re-begin below to force our baud

  Serial.begin(115200);
  while (!Serial) { delay(10); }   // native USB CDC: wait for host to open port
  delay(1000);                     // give yourself time to open the monitor

  analogReadResolution(12);        // 0..4095
  analogSetPinAttenuation(kAdcPin, ADC_11db); // full ~0..3.3V range

  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.setCursor(0, 0);
  M5.Display.setTextSize(1);
  M5.Display.println("STAGE A");
  M5.Display.println("boot OK");
  M5.Display.println("waiting for");
  M5.Display.println("first sample...");

  Serial.println("t_ms,adc_raw,adc_volts");
}

void loop() {
  // 8x oversample to average out ADC LSB noise -- cheap, worth doing even
  // at this "just checking wiring" stage.
  long sum = 0;
  for (int i = 0; i < 8; ++i) sum += analogRead(kAdcPin);
  int raw = sum / 8;

  // NOTE: 3.3f here is the *nominal* ADC reference, not a measured one.
  // Part of what this sanity check is FOR is finding out how far off that
  // assumption is from your multimeter -- don't fix this number until
  // you've actually compared the two and written the result down
  // (docs/sensor_choice.md). If they disagree by more than ~2%, that
  // mismatch is itself a data point, not a bug to silently correct here.
  float volts = raw * (3.3f / 4095.0f);

  Serial.printf("%lu,%d,%.4f\n", millis(), raw, volts);

  // Status readout only -- not the graded signal, just proof of life.
  // The toggling "*"/" " marker moves every sample so a frozen screen
  // (vs. a frozen board) is obvious even without watching the numbers.
  ++sampleCount;
  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.setCursor(0, 0);
  M5.Display.println("STAGE A -- OK");
  M5.Display.printf("raw:  %d\n", raw);
  M5.Display.printf("volts:%.4f\n", volts);
  M5.Display.printf("n:%lu %s\n", sampleCount, (sampleCount % 2) ? "*" : " ");

  delay(200); // slow on purpose -- this stage is for reading by eye
}
