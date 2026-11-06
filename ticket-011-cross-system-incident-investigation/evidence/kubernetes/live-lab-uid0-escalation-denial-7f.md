# Ticket 011 - AT-08 UID 0 Privilege Escalation Test

Classification: ACTUAL ISOLATED MINIKUBE LAB

Test: AT-08
Pod: reporting-api-598b9767f5-scfzw
Start UTC: 2026-11-03T18:42:35.7158221+00:00
End UTC: 2026-11-03T18:42:35.9703824+00:00

## Technique

Attempt to change the effective execution context
from non-root UID 10001 to UID 0 using Python
os.setuid(0).

## Expected Result

The Linux kernel denies the operation with EPERM.

## Actual Results

Security preflight passed: True
EPERM denial observed: True
Unexpected privilege gain: False
Python exit code: 0

Reporting container stable: True
Protected namespace unchanged: True

Outcome: PASS_UID0_ESCALATION_DENIED

## Safety and Limitations

No shell or interactive terminal was launched.
No Kubernetes resource specification was changed.
No credential or ServiceAccount token was read.

This tests one specific privilege-escalation
operation in the hardened reporting container.
It does not prove resistance to every possible
privilege-escalation technique.

The AT-08 result supplements seven previously
documented candidates. Formal acceptance of all
eight tests remains subject to ticket criteria.