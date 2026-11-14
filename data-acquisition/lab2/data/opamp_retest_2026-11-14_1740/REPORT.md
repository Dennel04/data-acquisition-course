# Op-amp retest 2026-11-14T17:40:37

**Verdict: FAIL**

- Port: `COM4`, firmware: `meter`
- Design: Rf 10.0 kOhm, Rref 53.8 kOhm, gain 1.186, Vref 0.428 V
- Volts are uncalibrated (Lab 1 factor 3.70 V / 4095). Pressure is not converted.

| Condition | Mean V | Min V | Max V | Noise mV | Samples | Expected V |
|---|---|---|---|---|---|---|
| atmosphere | 0.848 | 0.847 | 0.848 | 0.0 | 41 | 0.906 |
| full_suction | 0.233 | 0.229 | 0.237 | 2.4 | 42 | 0.300 |
| full_blowing | 1.128 | 1.088 | 1.206 | 23.6 | 41 | 2.767 |

| Result | Check | Detail |
|---|---|---|
| PASS | Output follows pressure | suction 0.233 V < atmosphere 0.848 V < blowing 1.128 V |
| FAIL | Output range | 0.89 V from full suction to full blowing (need >= 1.5 V, design 2.47 V) |
| PASS | Not stuck at the low end | full suction min 0.229 V, mean 0.233 V (need min >= 0.054 V and mean >= 0.10 V) |
| PASS | Safe for G5 at the high end | full blowing max 1.206 V (need <= 3.0 V) |
| PASS | Noise at atmosphere | 0.0 ADC codes = 0.0 mV standard deviation (aim <= 10 codes) |
| PASS | Close to design: atmosphere | 0.848 V vs 0.906 V expected (-0.058 V, allowed +-0.25 V) |
| PASS | Close to design: full_suction | 0.233 V vs 0.300 V expected (-0.067 V, allowed +-0.25 V) |
| WARN | Close to design: full_blowing | 1.128 V vs 2.767 V expected (-1.639 V, allowed +-0.25 V) |
| WARN | Implied gain | 0.430 vs design 1.186; assumes the pump reached the 14.11 sensor range 0.32-2.4 V |

Files: `opamp_retest.csv`, `summary.json`
