#include "sensor.h"

namespace sensor {

void begin() {
  analogReadResolution(12);
  analogSetPinAttenuation(kAdcPin, ADC_11db);
}

int readRawAdc() {
  long sum = 0;
  for (int i = 0; i < 8; ++i) sum += analogRead(kAdcPin);
  return sum / 8;
}

float adcReferenceVolts() {
  return 3.3f; // see the big comment in sensor.h -- verify, don't assume
}

float countsToVolts(int counts) {
  return counts * (adcReferenceVolts() / kAdcMaxCounts);
}

float voltsToAbsoluteKpa(float volts) {
  return (volts / kVcc - kTransferOffset) / kTransferSlope;
}

float toRelativeKpa(float absoluteKpa, float atmosphericKpa) {
  return absoluteKpa - atmosphericKpa;
}

} // namespace sensor
