#!/bin/sh
# Op-amp retest: double-click in Finder (or run ./run_opamp_retest.command). Creates .venv on first run.
cd "$(dirname "$0")" || exit 1
if [ ! -x .venv/bin/python ]; then
  echo "First run: setting up Python, takes a minute..."
  python3 -m venv .venv || { echo "Python 3 not found. Install it from https://www.python.org/downloads/"; exit 1; }
fi
.venv/bin/python -m pip install -q -r src/python/requirements.txt
.venv/bin/python src/python/opamp_retest.py "$@"
