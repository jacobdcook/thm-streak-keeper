@echo off
REM Creates a venv and installs deps for Windows.
python -m venv .venv
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
echo [+] Done. Use:  .venv\Scripts\python save_session.py   and   .venv\Scripts\python main_local.py
pause
