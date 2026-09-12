// Full firmware: Stage B (kPa + display) + Stage C (strict 10ms loop,
// CSV-shaped fields) + Stage D (JSON protocol + pump state machine) + a
// stub for the "letter" feature (part 5), all in one build.
//
// This is graded coursework (Lab 1, SVNC.00.325) -- know this code well
// enough to walk through it at the oral defense. See ../BUILD_NOTES.md
// for what's still a placeholder pending real hardware measurements.

#include <Arduino.h>
#include <M5Unified.h>
#include "sensor.h"
#include "pump_logic.h"
#include "comms.h"

namespace {

constexpr uint32_t kLoopPeriodMs = 10; // README: "iga 10 ms"

pump::Controller pumpController;
pump::Mode currentMode = pump::Mode::Off;

float atmosphericKpa = 0.0f; // measured once at startup, pump off, tubing open
uint32_t nextLoopAtMs = 0;

// --- Part 5 stub: short press cycles a letter, long press "sends" it. ---
// The actual channel/protocol for "Nutikad Lahendused" wasn't agreed yet
// when this was written (README: "lepitakse kokku esimesel nädalal") --
// fill in sendLetterToChannel() once your team knows the real transport
// (could be another UART line, MQTT via the PC bridge, etc).
char currentLetter = 'A';
constexpr uint32_t kLongPressMs = 600;

void sendLetterToChannel(char letter) {
  // TODO: replace with the real channel once agreed with "Nutikad Lahendused".
  Serial.printf("{\"letter\":\"%c\"}\n", letter);
}

void handleButton() {
  M5.update();
  // M5Unified's Button_Class already distinguishes a short click from a
  // long hold (default hold threshold ~600ms, matches kLongPressMs below
  // only if you set M5.BtnA.setHoldThresh(kLongPressMs) -- do that if you
  // want the exact number from this constant rather than the library default).
  if (M5.BtnA.wasClicked()) {
    currentLetter = (currentLetter == 'Z') ? 'A' : currentLetter + 1;
  }
  if (M5.BtnA.wasHold()) {
    sendLetterToChannel(currentLetter);
  }
}

void drawScreen(float pKpa, pump::Mode mode, bool pumpOn, const char* reason) {
  M5.Display.fillScreen(TFT_BLACK);
  M5.Display.setCursor(0, 0);
  M5.Display.setTextSize(1);
  M5.Display.printf("p: %.1f kPa\n", pKpa);
  M5.Display.printf("mode: %s\n",
                     mode == pump::Mode::Suction ? "suction"
                     : mode == pump::Mode::Blow   ? "blow"
                                                   : "off");
  M5.Display.printf("pump: %s\n", pumpOn ? "ON" : "off");
  M5.Display.printf("why: %s\n", reason);
  M5.Display.printf("letter: %c\n", currentLetter);
}

} // namespace

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);

  comms::begin(115200);
  sensor::begin();
  M5.BtnA.setHoldThresh(kLongPressMs);

  // Atmospheric baseline: tubing open, pump off, average a handful of
  // readings. If this runs before the tubing is actually open to air,
  // every relative-kPa value downstream will be offset -- worth a sanity
  // glance at the printed value before trusting it.
  long sum = 0;
  constexpr int kSamples = 32;
  for (int i = 0; i < kSamples; ++i) {
    sum += sensor::readRawAdc();
    delay(5);
  }
  float atmVolts = sensor::countsToVolts(sum / kSamples);
  atmosphericKpa = sensor::voltsToAbsoluteKpa(atmVolts);
  Serial.printf("# atmospheric baseline: %.2f kPa absolute\n", atmosphericKpa);

  pumpController.setMode(pump::Mode::Off);
  nextLoopAtMs = millis();
}

void loop() {
  // --- command intake (non-blocking) ---
  comms::Command cmd;
  if (comms::pollCommand(cmd)) {
    switch (cmd.type) {
      case comms::Command::Type::SetMode:
        currentMode = cmd.mode;
        pumpController.setMode(cmd.mode);
        break;
      case comms::Command::Type::SetBand:
        pumpController.setBand(cmd.band);
        break;
      case comms::Command::Type::Stop:
        currentMode = pump::Mode::Off;
        pumpController.setMode(pump::Mode::Off);
        break;
      default:
        break;
    }
  }

  handleButton();

  // --- strict 10ms cadence, non-blocking (no delay()) ---
  uint32_t now = millis();
  if ((int32_t)(now - nextLoopAtMs) < 0) return;
  nextLoopAtMs += kLoopPeriodMs;

  int raw = sensor::readRawAdc();
  float volts = sensor::countsToVolts(raw);
  float absKpa = sensor::voltsToAbsoluteKpa(volts);
  float relKpa = sensor::toRelativeKpa(absKpa, atmosphericKpa);

  char reason[12] = {0};
  bool pumpOn = pumpController.update(relKpa, now, reason);

  comms::sendTelemetry(now, raw, relKpa, currentMode, pumpOn);
  drawScreen(relKpa, currentMode, pumpOn, reason);
}
