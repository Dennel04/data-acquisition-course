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

constexpr uint32_t kLoopPeriodMs = 10; // README: "iga 10 ms" -- sensor read + JSON line, unchanged

// Display redraw is deliberately slower than the 10ms sensor loop: a full
// fillScreen()+redraw at 100Hz visibly flickers on this panel and buys
// nothing for a human reading it. Sensor read / kPa math / JSON telemetry
// still happen every 10ms as required; only the on-screen refresh is
// throttled. 12.09.26: flicker reported, fixed by decoupling this.
constexpr uint32_t kDisplayPeriodMs = 150;
uint32_t nextDisplayAtMs = 0;

// Residual flicker after throttling the refresh rate was root-caused to
// drawing straight to the panel: fillScreen()+printf() write visible
// pixels incrementally over SPI, so the blank-then-redraw is physically
// visible mid-frame. Fix (12.09.26, M5Stack's own recommended pattern --
// docs.m5stack.com/en/arduino/m5gfx/m5gfx_sprite): draw the whole frame
// into this off-screen sprite first, then push it to the panel in one
// transfer via pushSprite(). The viewer only ever sees a complete frame.
M5Canvas canvas(&M5.Display);

pump::Controller pumpController;
pump::Mode currentMode = pump::Mode::Off;

float atmosphericKpa = 0.0f; // measured once at startup, pump off, tubing open
uint32_t nextLoopAtMs = 0;

// --- Osa 5 ajutine kohalik asendus: lühike vajutus valib tähe ja pikk saadab. ---
// Smart Solutions püsivaras on tegelik kanal POST /api/letter. Selle pumba- ja
// rõhupüsivaraga ei ühendata Wi-Fi saatjat enne ühe AtomS3 riistvaraintegratsiooni.
// Praegune funktsioon kirjutab ainult lokaalse Serial-teate ega tõenda
// otsast lõpuni tähe edastamist.
char currentLetter = 'A';
constexpr uint32_t kLongPressMs = 600;

void sendLetterToChannel(char letter) {
  // TODO: ühenda Smart Solutions HTTP-saatja ühe AtomS3 riistvarakatses.
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
  // Draw into the off-screen sprite, not M5.Display, directly -- see the
  // canvas comment near the top of the file for why.
  canvas.fillScreen(TFT_BLACK);
  canvas.setCursor(0, 0);
  canvas.setTextSize(1.5f); // 1 was too small, 2 flickered/felt too big -- 12.09.26
  canvas.printf("p: %.1f kPa\n", pKpa);
  canvas.printf("mode: %s\n",
                mode == pump::Mode::Suction ? "suction"
                : mode == pump::Mode::Blow  ? "blow"
                                             : "off");
  canvas.printf("pump: %s\n", pumpOn ? "ON" : "off");
  canvas.printf("why: %s\n", reason);
  canvas.printf("letter: %c\n", currentLetter);
  canvas.pushSprite(0, 0); // one complete transfer -- this is what kills the flicker
}

} // namespace

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);

  comms::begin(115200);
  sensor::begin();
  M5.BtnA.setHoldThresh(kLongPressMs);

  // Off-screen buffer, same size/color depth as the panel -- must be
  // created after M5.begin() so M5.Display.width()/height() are valid.
  canvas.setColorDepth(M5.Display.getColorDepth());
  canvas.createSprite(M5.Display.width(), M5.Display.height());

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
      case comms::Command::Type::SetLimits:
        pumpController.setSafetyLimits(cmd.limits);
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

  // Screen refresh throttled separately from the 10ms sensor/JSON cadence
  // above -- see kDisplayPeriodMs comment near the top of the file.
  if ((int32_t)(now - nextDisplayAtMs) >= 0) {
    nextDisplayAtMs = now + kDisplayPeriodMs;
    drawScreen(relKpa, currentMode, pumpOn, reason);
  }
}
