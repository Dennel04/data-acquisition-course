#pragma once
#include <cstdint>
#include <cstring>

// Bang-bang / hysteresis controller matching README part 4's pseudocode:
//
//   suction: if p weaker than "on" AND idle-time >= min-off-time -> pump 1
//            if p stronger than "off"                            -> pump 0
//   blow:    same shape, opposite sign
//   off / out-of-scale / cycles-per-min over limit -> pump 0, reason shown
//
// The actual on/off kPa thresholds, min-off-time and max-cycles/min are
// NOT hardcoded here -- those five numbers are what part 4 asks the team
// to measure (holding curves on glass / in air / capped tube) and record
// in docs/pump_control.md. This class only implements the *shape* of the
// control law; you supply the numbers via setBand()/setSafetyLimits().
namespace pump {

enum class Mode { Off, Suction, Blow };

struct Band {
  float onKpa = 0;   // relative kPa: weaker-than-this starts the pump
  float offKpa = 0;  // relative kPa: stronger-than-this stops the pump
};

struct SafetyLimits {
  uint32_t minOffTimeMs = 0;     // don't restart before this much idle time
  uint16_t maxCyclesPerMin = 0;  // 0 = no limit; else a hard safety cutoff
  float outOfScaleAbsKpa = 200;  // |p| beyond this -> treat as sensor fault
};

class Controller {
 public:
  void setMode(Mode m) {
    if (m != mode_) {
      mode_ = m;
      pumpOn_ = false;
    }
  }
  void setBand(const Band& b) { band_ = b; }
  void setSafetyLimits(const SafetyLimits& s) { limits_ = s; }

  // Call every 10ms with the latest relative-kPa reading. Writes a short
  // reason string (for screen/log) into reasonOut, which must hold at
  // least 12 bytes including the terminator.
  bool update(float pKpa, uint32_t nowMs, char* reasonOut) {
    auto setReason = [&](const char* r) {
      if (reasonOut) std::strncpy(reasonOut, r, 11);
    };

    if (mode_ == Mode::Off) {
      pumpOn_ = false;
      setReason("off");
      return false;
    }

    if (pKpa > limits_.outOfScaleAbsKpa || pKpa < -limits_.outOfScaleAbsKpa) {
      pumpOn_ = false;
      setReason("out-of-scale");
      return false;
    }

    if (limits_.maxCyclesPerMin > 0) {
      if (nowMs - cycleWindowStartMs_ > 60000) {
        cycleWindowStartMs_ = nowMs;
        cyclesThisWindow_ = 0;
      }
      if (cyclesThisWindow_ > limits_.maxCyclesPerMin) {
        pumpOn_ = false;
        setReason("cycle-limit");
        return false;
      }
    }

    const bool suction = (mode_ == Mode::Suction);
    const bool weakerThanOn =
        suction ? (pKpa > band_.onKpa) : (pKpa < band_.onKpa);
    const bool strongerThanOff =
        suction ? (pKpa < band_.offKpa) : (pKpa > band_.offKpa);

    bool wantOn = pumpOn_;
    if (!pumpOn_) {
      const bool idleLongEnough =
          (nowMs - lastOffAtMs_) >= limits_.minOffTimeMs;
      if (weakerThanOn && idleLongEnough) wantOn = true;
    } else {
      if (strongerThanOff) wantOn = false;
    }

    if (wantOn != pumpOn_) {
      if (!wantOn) {
        lastOffAtMs_ = nowMs;
        ++cyclesThisWindow_;
      }
      pumpOn_ = wantOn;
    }

    setReason(pumpOn_ ? (suction ? "suction" : "blow") : "band-hold");
    return pumpOn_;
  }

 private:
  Mode mode_ = Mode::Off;
  Band band_;
  SafetyLimits limits_;

  bool pumpOn_ = false;
  uint32_t lastOffAtMs_ = 0;
  uint32_t cycleWindowStartMs_ = 0;
  uint16_t cyclesThisWindow_ = 0;
};

} // namespace pump
