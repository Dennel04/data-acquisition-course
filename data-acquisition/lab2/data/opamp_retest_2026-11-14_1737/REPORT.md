# Op-amp retest 2026-11-14T17:37:05

**Verdict: FAIL**

- Port: `COM4`, firmware: `meter`
- Design: Rf 10.0 kOhm, Rref 53.8 kOhm, gain 1.186, Vref 0.428 V
- Volts are uncalibrated (Lab 1 factor 3.70 V / 4095). Pressure is not converted.

| Condition | Mean V | Min V | Max V | Noise mV | Samples | Expected V |
|---|---|---|---|---|---|---|
| atmosphere | 0.847 | 0.847 | 0.848 | 0.4 | 42 | 0.906 |
| full_suction | 0.849 | 0.848 | 0.851 | 1.0 | 41 | 0.300 |
| full_blowing | 0.847 | 0.847 | 0.848 | 0.3 | 42 | 2.767 |

| Result | Check | Detail |
|---|---|---|
| FAIL | Output follows pressure | suction 0.849 V < atmosphere 0.847 V < blowing 0.847 V (expected at least 0.2 V between each) |
| FAIL | Output range | -0.00 V from full suction to full blowing (need >= 1.5 V, design 2.47 V) |
| PASS | Not stuck at the low end | full suction min 0.848 V, mean 0.849 V (need min >= 0.054 V and mean >= 0.10 V) |
| PASS | Safe for G5 at the high end | full blowing max 0.848 V (need <= 3.0 V) |
| PASS | Noise at atmosphere | 0.4 ADC codes = 0.4 mV standard deviation (aim <= 10 codes) |
| PASS | Close to design: atmosphere | 0.847 V vs 0.906 V expected (-0.059 V, allowed +-0.25 V) |
| WARN | Close to design: full_suction | 0.849 V vs 0.300 V expected (+0.549 V, allowed +-0.25 V) |
| WARN | Close to design: full_blowing | 0.847 V vs 2.767 V expected (-1.919 V, allowed +-0.25 V) |
| WARN | Implied gain | -0.001 vs design 1.186; assumes the pump reached the 14.11 sensor range 0.32-2.4 V |

Files: `opamp_retest.csv`, `summary.json`
