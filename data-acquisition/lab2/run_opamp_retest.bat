@echo off
rem Op-amp retest: double-click this file. Creates .venv on first run.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo First run: setting up Python, takes a minute...
  py -3 -m venv .venv 2>nul || python -m venv .venv
)
if not exist .venv\Scripts\python.exe (
  echo Python 3 was not found. Install it from https://www.python.org/downloads/ and run this again.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pip install -q -r src\python\requirements.txt
.venv\Scripts\python.exe src\python\opamp_retest.py %*
pause
