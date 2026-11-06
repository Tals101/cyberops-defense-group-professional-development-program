# Ticket 011 - Enhancement 2 Negative Control

Classification: ACTUAL MINIKUBE LAB

Rule: Ticket011 Reporting ServiceAccount Token Access Attempt
Falco Helm revision: 3

Reporting Pod: reporting-api-598b9767f5-scfzw
Falco Pod: ticket011-falco-mclt8

Start UTC: 2026-11-03T18:17:38.0349240+00:00
End UTC: 2026-11-03T18:17:38.7967566+00:00

## Benign Test

Operation: Direct Python HTTP GET /health
HTTP result: 200
Python exit code: 0

Token path accessed: NO
Shell launched: NO
Terminal attached: NO

## Falco Results

Previous positive control: DETECTED_AND_ATTRIBUTED_FAILED_OPEN
Custom-rule events: 0
Attributed reporting-container events: 0
Invalid event timestamps: 0
Log window truncated: False
Falco stable: True

Outcome: PASS_NO_TOKEN_ACCESS_ALERT

## Interpretation

A PASS demonstrates that this specific benign
health-check operation did not trigger the
ServiceAccount token-access rule.

It does not prove a general false-positive rate.

No credentials were accessed.
No Kubernetes resource specifications changed.