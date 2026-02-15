#!/usr/bin/env bash
# Run THM streak bot headless. Use with cron for daily run.
cd "$(dirname "$0")"
export THM_HEADLESS=1
.venv/bin/python3 main_local.py >> tryhackmebot.log 2>&1
