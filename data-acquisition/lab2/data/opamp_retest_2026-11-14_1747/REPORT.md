# Op-amp retest 2026-11-14T17:47:13

**Verdict: PASS**

- Port: `COM4`, firmware: `meter`
- Design: Rf 10.0 kOhm, Rref 53.8 kOhm, gain 1.186, Vref 0.428 V
- Volts are uncalibrated (Lab 1 factor 3.70 V / 4095). Pressure is not converted.

| Condition | Mean V | Min V | Max V | Noise mV | Samples | Expected V |
|---|---|---|---|---|---|---|
| atmosphere | 0.858 | 0.857 | 0.858 | 0.4 | 41 | 0.906 |
| full_suction | 0.236 | 0.228 | 0.239 | 1.8 | 40 | 0.300 |
| full_blowing | 2.664 | 2.210 | 2.686 | 8.5 | 42 | 2.767 |

| Result | Check | Detail |
|---|---|---|
| PASS | Output follows pressure | suction 0.236 V < atmosphere 0.858 V < blowing 2.664 V |
| PASS | Output range | 2.43 V from full suction to full blowing (need >= 1.5 V, design 2.47 V) |
| PASS | Not stuck at the low end | full suction min 0.228 V, mean 0.236 V (need min >= 0.054 V and mean >= 0.10 V) |
| PASS | Safe for G5 at the high end | full blowing max 2.686 V (need <= 3.0 V) |
| PASS | Noise at atmosphere | 0.5 ADC codes = 0.4 mV standard deviation (aim <= 10 codes) |
| PASS | Close to design: atmosphere | 0.858 V vs 0.906 V expected (-0.048 V, allowed +-0.25 V) |
| PASS | Close to design: full_suction | 0.236 V vs 0.300 V expected (-0.064 V, allowed +-0.25 V) |
| PASS | Close to design: full_blowing | 2.664 V vs 2.767 V expected (-0.102 V, allowed +-0.25 V) |
| PASS | Implied gain | 1.168 vs design 1.186; assumes the pump reached the 14.11 sensor range 0.32-2.4 V |

Files: `opamp_retest.csv`, `summary.json`
