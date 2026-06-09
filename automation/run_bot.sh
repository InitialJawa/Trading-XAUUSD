#!/bin/bash
# XAUUSD Trading Bot - Automation Script
# Run this via cron or systemd for unattended operation

BOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$BOT_DIR/logs"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] XAUUSD Bot Starting..." >> "$LOG_DIR/bot_cron.log"

cd "$BOT_DIR" || exit 1

# Activate virtual environment if exists
if [ -f "$BOT_DIR/.venv/bin/activate" ]; then
    source "$BOT_DIR/.venv/bin/activate"
elif [ -f "$BOT_DIR/venv/bin/activate" ]; then
    source "$BOT_DIR/venv/bin/activate"
fi

# Run pipeline
python -m trading_bot.run_pipeline "$@" >> "$LOG_DIR/bot_cron.log" 2>&1

if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] Pipeline completed successfully" >> "$LOG_DIR/bot_cron.log"
else
    echo "[$TIMESTAMP] Pipeline FAILED" >> "$LOG_DIR/bot_cron.log"
fi
