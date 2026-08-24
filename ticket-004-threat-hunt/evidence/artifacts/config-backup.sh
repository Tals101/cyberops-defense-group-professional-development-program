#!/bin/bash

BACKUP_DIR="/var/tmp"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
OUTPUT="${BACKUP_DIR}/dev-config-${TIMESTAMP}.tar.gz"

tar -czf "$OUTPUT" \
    /etc/hosts \
    /etc/ssh/sshd_config 2>/dev/null

chmod 600 "$OUTPUT"
