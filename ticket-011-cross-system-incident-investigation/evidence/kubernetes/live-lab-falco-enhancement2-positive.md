# Ticket 011 - Enhancement 2 Positive Control

Classification: ACTUAL MINIKUBE LAB

Rule: Ticket011 Reporting ServiceAccount Token Access Attempt
Falco Helm revision: 3

Reporting Pod: reporting-api-598b9767f5-scfzw
Falco Pod: ticket011-falco-mclt8

Start UTC: 2026-11-03T18:14:21.1120659+00:00
End UTC: 2026-11-03T18:14:21.4302822+00:00

## Controlled Stimulus

ServiceAccount token automount: DISABLED
ServiceAccount volume mount: ABSENT
Token path before attempt: ABSENT

Operation: Python os.open against token path
Result: ENOENT (file not found)
Token contents read: NO
Shell or TTY: NO

## Falco Observations

Custom-rule candidate events: 1
Attributed reporting-container events: 1
Invalid event timestamps: 0
Log window truncated: False
Falco sensor stable: True

Outcome: DETECTED_AND_ATTRIBUTED_FAILED_OPEN

## Interpretation

This test evaluates detection of a failed
ServiceAccount token-path access attempt.

It does not demonstrate that a token existed,
was read, or was exfiltrated.

Only scoped Ticket 011 alert metadata was saved.
Unrelated Falco event bodies were not retained.

No Kubernetes resource specifications were changed.