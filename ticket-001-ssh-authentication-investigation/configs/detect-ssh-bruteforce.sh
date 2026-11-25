#!/bin/bash

THRESHOLD=5
TIME_WINDOW="5 minutes ago"

journalctl -u ssh --since "$TIME_WINDOW" --no-pager |
grep "Failed password" |
awk '{
    for (i = 1; i <= NF; i++) {
        if ($i == "from") {
            print $(i + 1)
        }
    }
}' |
sort |
uniq -c |
while read -r count ip
do
    if [ "$count" -ge "$THRESHOLD" ]; then
        logger -p auth.warning -t ssh-bruteforce \
        "ALERT: $count failed SSH login attempts from $ip during the last 5 minutes"
    fi
done
