#!/usr/bin/env bash
# Run once. Creates a venv and installs deps (avoids externally-managed-environment).
cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
echo "[+] Done. Use:  .venv/bin/python3 save_session.py   and   .venv/bin/python3 main_local.py"
