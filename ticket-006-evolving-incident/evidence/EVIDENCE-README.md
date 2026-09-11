# Ticket #006 — Evidence Package

## Purpose

This package contains preserved incident evidence, derived analysis artifacts, and supporting technical material used during the investigation of FIN-WS17.

Pretest data is intentionally excluded from final incident attribution.

## Primary Incident Evidence

### fin-ws17-final-audit.log

Preserved auditd telemetry from FIN-WS17.

Used to establish:

- Process execution.
- File access.
- Archive creation.
- curl execution.
- Temporary-file deletion.
- User and audit identity context.

### fin-ws17-final-https.pcap

Preserved packet capture of HTTPS communications involving the simulated external destination.

Used to establish:

- Outbound network sessions.
- Timing of communications.
- Repeated HTTPS activity.

### SHA256SUMS.txt

Original checksum manifest for the Ubuntu-side final audit log and packet capture.

## External Server Evidence

Located under:

`evidence/external-server/`

### server.log

Server-side connection log from the preserved final scenario run.

Used to establish:

- POST activity from FIN-WS17.
- `/api/report` request.
- `/api/cache` request.
- Uploaded byte counts.

### received-data.bin

Raw concatenated POST bodies received by the external server.

Used to demonstrate successful external receipt of transmitted data.

### cache-body.bin

Derived analysis artifact containing the separated archive body from the suspicious `/api/cache` transfer.

### report-body.bin

Derived analysis artifact containing the separated body from the documented `/api/report` transfer.

### Q3_budget.csv

Finance file extracted from the externally received archive.

Its SHA-256 matches the preserved original Finance file.

### vendor_payments.csv

Finance file extracted from the externally received archive.

Its SHA-256 matches the preserved original Finance file.

### server.py

Preserved external-server source code.

Used to establish that the receiving service stores uploaded data and performs no observable financial-data conversion.

### server.crt

Preserved TLS certificate used by the external service.

Used to establish:

- CN `finance-sync.local`
- Self-signed certificate status.
- Certificate validity period.
- Service identity could not be independently authenticated through the certificate.

### SHA256SUMS-FINAL.txt

Final checksum manifest for the external-server evidence and derived analysis artifacts copied into the Ubuntu closure workspace.

All listed files were successfully verified using `sha256sum -c`.

## Supporting Evidence

### ../scripts/document_cache.sh

Preserved copy of the questioned utility.

SHA-256:

`1ee17971ce3cfb330457383ed019631b12ef9a8d738c560b1aad795329ee0c1c`

Used for static analysis.

### ../scripts/finance_sync.sh

Preserved copy of the documented Finance synchronization workflow used for comparison.

### ../logs/soc-alert-0917.txt

Synthetic initial SOC alert used to establish the starting information available at 09:17.

### ../fin-ws17/system-profile.txt

Lab system profile and documented workflow context.

### ../fin-ws17/simulation-time-note.txt

Explains the distinction between fictional scenario times and actual lab-generation timestamps.

### ../fin-ws17/synthetic-data/

Preserved synthetic Finance data used in the lab.

## Evidence Classification

### Original / Primary Evidence

- fin-ws17-final-audit.log
- fin-ws17-final-https.pcap
- external-server/server.log
- external-server/received-data.bin
- external-server/server.crt

### Preserved Supporting Artifacts

- scripts/document_cache.sh
- scripts/finance_sync.sh
- external-server/server.py
- logs/soc-alert-0917.txt
- fin-ws17/system-profile.txt
- fin-ws17/simulation-time-note.txt

### Derived Analysis Artifacts

- external-server/cache-body.bin
- external-server/report-body.bin
- external-server/Q3_budget.csv
- external-server/vendor_payments.csv

Derived artifacts were produced from preserved evidence for analysis and are not represented as original endpoint files.

## Excluded from Final Incident Attribution

The following lab setup or pretest artifacts are excluded from incident attribution:

- `pretest/`
- Kali `pretest/`
- Kali `pretest-initial/`
- Python `__pycache__`
- Private TLS key `server.key`

These materials were part of lab construction or testing and should not be treated as incident evidence.

## Integrity

Ubuntu primary evidence is protected by its existing SHA-256 manifest.

External-server evidence is protected by:

`external-server/SHA256SUMS-FINAL.txt`

All final external-server checksum validations returned `OK`.
