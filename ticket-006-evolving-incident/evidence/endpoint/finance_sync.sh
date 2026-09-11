#!/bin/bash

REPORT="/home/mreynolds/Reports/daily_summary.txt"

curl -k -s \
  -X POST \
  --data-binary @"$REPORT" \
  https://finance-sync.local/api/report \
  -o /home/mreynolds/Reports/sync-response.txt
