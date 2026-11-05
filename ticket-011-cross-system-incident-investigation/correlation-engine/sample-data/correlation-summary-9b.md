# Ticket 011 - Initial Synthetic Cross-System Correlation

**Classification: SYNTHETIC LABORATORY DATA ONLY**

Original files were not modified. Source SHA256 hashes were checked.

- Source datasets: 7
- Normalized synthetic events: 42
- Cross-system shared-IP groups: 2
- Cross-system five-minute IP pairs: 37
- Cross-system causation: NOT ESTABLISHED

## Shared-address candidate groups

- `203.0.113.77`: AWS, KUBERNETES, LINUX (12 source/destination occurrences)
- `203.0.113.88`: AWS, LINUX (2 source/destination occurrences)

## Evidence interpretation

Each normalized record retains its original event ID,
timestamp, source file, source line number, and SHA256.
Source and destination IP directions are preserved.

Shared IPs and five-minute pairs are candidate associations.
They do not prove shared identity, compromise, or causation.
Independent attribution and network mapping are required.

## Next validation

Test schema variations, corrupted source hashes,
invalid timestamps, missing event IDs, and false matches.
