#pragma once
#include <cstdint>
#include <cstring>

namespace acquisition {
constexpr uint32_t kPeriodMs = 10;
inline bool validConfig(const char* s) {
  return s && (!std::strcmp(s, "raw") || !std::strcmp(s, "opamp"));
}
inline bool validRun(const char* s) {
  if (!s || std::strlen(s) != 16) return false;
  for (int i=0; i<16; ++i)
    if (!((s[i]>='0' && s[i]<='9') || (s[i]>='a' && s[i]<='f'))) return false;
  return true;
}
// Lab 1's 10 ms millis cadence; skip overdue slots rather than invent a burst
// of historical samples. Timestamp always belongs to the actual ADC read.
struct Clock {
  uint32_t next = 0, missed = 0;
  void start(uint32_t now) { next=now; missed=0; }
  bool due(uint32_t now) {
    if (static_cast<int32_t>(now-next) < 0) return false;
    const uint32_t skipped = (now-next)/kPeriodMs;
    missed += skipped;
    next += (skipped+1)*kPeriodMs;
    return true;
  }
};
}  // namespace acquisition
