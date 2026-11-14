# Op-amp retest 2026-11-14T17:45:30

**Verdict: PASS**

- Port: `COM4`, firmware: `meter`
- Design: Rf 10.0 kOhm, Rref 53.8 kOhm, gain 1.186, Vref 0.428 V
- Volts are uncalibrated (Lab 1 factor 3.70 V / 4095). Pressure is not converted.

| Condition | Mean V | Min V | Max V | Noise mV | Samples | Expected V |
|---|---|---|---|---|---|---|
| atmosphere | 0.849 | 0.848 | 0.849 | 0.2 | 41 | 0.906 |
| full_suction | 0.407 | 0.228 | 0.849 | 276.2 | 41 | 0.300 |
| full_blowing | 2.669 | 2.653 | 2.691 | 6.5 | 42 | 2.767 |

| Result | Check | Detail |
|---|---|---|
| PASS | Output follows pressure | suction 0.407 V < atmosphere 0.849 V < blowing 2.669 V |
| PASS | Output range | 2.26 V from full suction to full blowing (need >= 1.5 V, design 2.47 V) |
| PASS | Not stuck at the low end | full suction min 0.228 V, mean 0.407 V (need min >= 0.054 V and mean >= 0.10 V) |
| PASS | Safe for G5 at the high end | full blowing max 2.691 V (need <= 3.0 V) |
| PASS | Noise at atmosphere | 0.3 ADC codes = 0.2 mV standard deviation (aim <= 10 codes) |
| PASS | Close to design: atmosphere | 0.849 V vs 0.906 V expected (-0.057 V, allowed +-0.25 V) |
| PASS | Close to design: full_suction | 0.407 V vs 0.300 V expected (+0.107 V, allowed +-0.25 V) |
| PASS | Close to design: full_blowing | 2.669 V vs 2.767 V expected (-0.098 V, allowed +-0.25 V) |
| PASS | Implied gain | 1.087 vs design 1.186; assumes the pump reached the 14.11 sensor range 0.32-2.4 V |

Files: `opamp_retest.csv`, `summary.json`
