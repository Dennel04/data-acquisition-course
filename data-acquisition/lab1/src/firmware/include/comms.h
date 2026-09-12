#pragma once
#include <Arduino.h>
#include "pump_logic.h"

// Wire protocol, exactly as specified in README part 4:
//   Atom -> PC:  {"t":123456,"adc":2011,"p":-52.3,"mode":"suction","pump":1}
//   PC -> Atom:  {"cmd":"mode","mode":"suction"}
//                {"cmd":"band","on":-40,"off":-60}
//                {"cmd":"stop"}
namespace comms {

struct Command {
  enum class Type { None, SetMode, SetBand, Stop } type = Type::None;
  pump::Mode mode = pump::Mode::Off;
  pump::Band band;
};

void begin(unsigned long baud);

// Non-blocking; call once per loop iteration. Returns true if a full line
// was received and parsed into outCmd. Malformed/partial lines are
// dropped (returns false) rather than blocking the 10ms loop.
bool pollCommand(Command& outCmd);

void sendTelemetry(uint32_t tMs, int adcRaw, float pKpa, pump::Mode mode,
                    bool pumpOn);

} // namespace comms
