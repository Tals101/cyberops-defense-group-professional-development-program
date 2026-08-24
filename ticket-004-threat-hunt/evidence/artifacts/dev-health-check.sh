#!/bin/bash

LOG_FILE="/var/log/dev-health-check.log"

{
    echo "===== Health Check ====="
    echo "Timestamp: $(date --iso-8601=seconds)"
    echo "Hostname: $(hostname)"
    echo
    echo "Uptime:"
    uptime
    echo
    echo "Disk Usage:"
    df -h /
    echo
} >> "$LOG_FILE"
