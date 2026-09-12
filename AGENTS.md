# AGENTS.md — Data Acquisition course repo

This repo belongs to a 3-student team working through the "Data
Acquisition" (Andmehõive, SVNC.00.325) labs. One repo covers the whole
course; each lab gets its own folder under `data-acquisition/labN/`.

## What this course is building toward

Five MG400 robots in the lab, five vacuum-pump boxes. One factory box is
"smart" (measures pressure, stops the pump when reached); the other four
just run while the DO line is up. The course's job: make all five behave
like the smart one. Each output tube gets its own pressure sensor, an
AtomS3 (ESP32) shows pressure + decision on its screen, and a Python
script on the computer reads the Atom over UART-USB and drives the pump
via the MG400's DO line. By year end this logic moves onto a custom PCB;
right now it's breadboarded, where a mistake costs one wire.

Same team, same MG400, same AtomS3 as the other two courses running in
parallel (3D Printing & CAD, "Smart Solutions"/programming) — one shared
demo across all three: **press a key on the AtomS3, the robot draws that
letter.** This course's contribution is the pressure-sensing/pump-control
logic; the letter-select/robot-draw logic is the other courses' repos. See
the user's other course repo: `3d-printing-course`.

## Repo layout

```
data-acquisition/
  lab1/
    README.md    <- official Estonian assignment, copied verbatim, filled in as work happens (KAARDISTA ISE sections)
    src/         <- AtomS3 firmware + Python logger/pump-control code
    data/        <- CSV logs
    notebooks/   <- Jupyter notebooks: spectra, statistics
    docs/        <- sensor_choice.md, bom.md, pump_control.md, schematic photos, oscilloscope shots, Falstad exports
study-ru/
  lab1-translation.md   <- personal Russian translation, NOT part of the graded submission
```

Each later lab under `data-acquisition/labN/` follows the same pattern.

## Conventions

- **Language:** assignments are issued in Estonian. `README.md` in each lab
  folder stays in Estonian (official template, `KAARDISTA ISE` = "map it
  yourself" fill-in-the-blank sections) — filled in as the student
  measures things. Personal Russian translations live only under
  `study-ru/`, never touching the graded files.
- **Nothing gets deleted.** A wrong measurement stays in the doc with its
  date; the correction goes underneath it, not over it.
- **Devlog entries** live inside each lab's `README.md` under
  "Arenduspäevik" — one entry per work session, appended (not edited
  later).
- Diagrams/simulations go into the doc as an image + a link to the live,
  editable file (Falstad circuit link, draw.io link).
- Git tag per lab on submission, e.g. `data-acquisition-lab1`.

## Tools in play

- AtomS3 (ESP32) — Arduino IDE or PlatformIO firmware.
- Python 3 + pyserial for the logger/pump-control script; Jupyter Lab +
  numpy/pandas/scipy/matplotlib for analysis (spectra via `scipy.signal`,
  FFT).
- Falstad (circuit simulation), draw.io (system diagrams).
- MG400 base Python package: https://github.com/KKallas/mg400-base
- Oscilloscope with FFT, multimeter, breadboard.

## Safety notes (for anyone, human or agent, drafting instructions)

- ADC pin doesn't tolerate 5V — check sensor output range against pin
  datasheet limits before wiring.
- Pump box is 24V; DO lines get connected only with the robot disabled
  and the box unpowered.
- Pump motor isn't built for once-a-second cycling — respect the
  minimum off-time before narrowing the control band.
- Open tubing at +110 kPa can fling loose — never point it at anyone.
- Hands off the table while the MG400 is powered; first run of anything
  new goes slow with e-stop in reach.
- No soldering in this lab.

## For an AI agent picking up work here

- Check the current lab's `README.md` first — live goals, checklist, and
  devlog are there; don't duplicate what's already answered.
- This is coursework: the student does the actual measurements/design
  work themselves. Help with translation, explaining concepts, repo/tool
  setup — don't produce the graded numbers, sensor choice, or devlog
  entries for them.
- If asked to translate assignment text, translate faithfully; don't
  editorialize instructor requirements.
