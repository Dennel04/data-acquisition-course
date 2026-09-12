# Lab 1 — build notes

This is the working firmware/logger for the lab (moved here from an
earlier reference draft in `study-ru/`). Before your defense (15-minute
oral conversation, teacher asks how you built it), make sure you can
actually walk through what's below — it's the "working files" grading
criterion, and the questions will be about this code specifically.

**Numbers this code does NOT and cannot supply on its own:** ADC
reference calibration, sensor choice, and the five pump-control numbers
(on/off kPa, min-off-time, max-cycles/min) all come from measuring the
real hardware in front of you — a multimeter/oscilloscope reading, or
logging the factory smart box's actual switch points. Nothing written
here can stand in for that; the placeholders below exist so you don't
lose track of what still needs a real measurement.

## What's here, staged like the assignment

- **`firmware_stageA_sanity/`** — README part 2's very first step: raw
  ADC on G5 → Serial, no display, no timing loop, no kPa math yet. Point
  of this stage is purely comparing the printed ADC-derived voltage
  against a multimeter reading of Vout, before building anything on top.
- **`firmware/`** — everything else: `sensor.h/.cpp` (ADC read + MPX5700AP
  transfer function), `pump_logic.h/.cpp` (the suction/blow hysteresis
  state machine from part 4's pseudocode), `comms.h/.cpp` (the JSON wire
  protocol), `main.cpp` (10ms loop, display, button/letter stub).
- **`python/logger.py`** — reads the Atom's JSON telemetry, writes the
  `t_ms, adc, p_kpa, pump` CSV (part 2), sends mode/band commands (part
  4), drives the MG400 pump box over `mg400-base`'s HTTP API, enforces
  the 500ms watchdog.

## Things this code deliberately does NOT decide for you

- **ADC reference voltage** (`sensor::adcReferenceVolts()`): hardcoded to
  the nominal 3.3V with a comment saying so. The whole point of the
  "matches multimeter within 2%" check is finding out whether that
  assumption holds on your actual board — recorded research turned up
  real accuracy caveats with ESP32's calibrated-mV API (avg ~45mV error,
  worse above 2.5V) that make "just call `analogReadMilliVolts()` and
  trust it" not obviously good enough for a 2% target either. Measure,
  don't assume either way.
- **Pump control numbers** (`on`/`off` kPa, min-off-time, max-cycles/min):
  passed in as required CLI args to `logger.py`, not hardcoded — these are
  literally the five numbers part 4 asks your team to measure from the
  three holding-curve scenarios.
- **Sensor choice** (part 1): this code assumes MPX5700AP throughout,
  since that's the day-1 starting point; the order decision itself isn't
  addressed here at all.
- **The letter channel** (part 5): `sendLetterToChannel()` is a stub that
  just prints JSON to Serial — the real transport is still "agreed in
  week 1" per the assignment, unknown at the time this was written.

## Verified vs. uncertain (so you know what to double-check)

Checked directly against sources during writing:
- AtomS3(R) needs `-DARDUINO_USB_CDC_ON_BOOT=1 -DARDUINO_USB_MODE=1` build
  flags for native-USB Serial to work —
  [docs.m5stack.com/en/core/AtomS3](https://docs.m5stack.com/en/core/AtomS3).
- G5 is a valid ADC1 pin on ESP32-S3 (ADC1_CH4), available for expansion
  on both AtomS3 and AtomS3R —
  [docs.m5stack.com/en/core/AtomS3](https://docs.m5stack.com/en/core/AtomS3),
  [docs.m5stack.com/en/core/AtomS3R](https://docs.m5stack.com/en/core/AtomS3R).
- PlatformIO board id `m5stack-atoms3` —
  [docs.platformio.org/en/latest/boards/espressif32/m5stack-atoms3.html](https://docs.platformio.org/en/latest/boards/espressif32/m5stack-atoms3.html).
  No dedicated `...atoms3r` board exists in the mainline
  `platform-espressif32` registry as of this writing — using the plain
  `atoms3` config and verifying on first flash.
- `mg400-base` HTTP API: `mg400 serve` on `localhost:8000`,
  `POST /api/pump {"mode":"suck"|"blow"|"off"}` —
  [github.com/KKallas/mg400-base](https://github.com/KKallas/mg400-base).
- `analogReadMilliVolts()` accuracy caveats (avg ~45mV error, worse near
  2.5–3V on ESP32-S3) — reported in
  [espressif/arduino-esp32#11041](https://github.com/espressif/arduino-esp32/issues/11041)
  and [#4941](https://github.com/espressif/arduino-esp32/issues/4941);
  motivated using raw `analogRead()` + your own measured reference here
  instead of that API, but re-check this against your own bench numbers.

Not independently verified — check before relying on them:
- Whether AtomS3R's display is GC9107 or ST7735 (m5-docs shows GC9107 on
  the AtomS3R page fetched one way and ST7735 "updated May 2026" another
  way — M5Unified is supposed to auto-detect this per-board, but if
  `M5.Display` init misbehaves, this is the first thing to check).
- Exact `mg400 do`/`mg400 pump` Python driver method names beyond the CLI
  and HTTP API — `logger.py` uses the HTTP API specifically because that
  surface was confirmed, not the in-process driver class.
- `bblanchon/ArduinoJson @ ^7.2.0` and `m5stack/M5Unified @ ^0.2.2` version
  pins are reasonable-as-of-writing guesses, not verified against the PlatformIO
  registry's actual latest releases — bump them if `pio lib install` complains.

## Suggested order to work through it

1. Flash `firmware_stageA_sanity/`, compare against multimeter, decide/
   record your ADC reference in your own `sensor_choice.md` numbers.
2. Read `firmware/include/sensor.h` + `.cpp`, understand the transfer
   function inversion well enough to explain it at defense.
3. Read `pump_logic.h`, trace through the suction-mode example by hand
   against the three holding scenarios in part 4 before trusting it.
4. Read `comms.h/.cpp` + `main.cpp`, understand the 10ms non-blocking
   loop pattern (`nextLoopAtMs`) — this is the part most tutorials get
   wrong by using blocking `delay(10)`, which drifts under load.
5. Read `python/logger.py`, run it with `--dry-run` first (no MG400 calls)
   against just the Atom, confirm the CSV looks right, then wire in the
   real pump box.
