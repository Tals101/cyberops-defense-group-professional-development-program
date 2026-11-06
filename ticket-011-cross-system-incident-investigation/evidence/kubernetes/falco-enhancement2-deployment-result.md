# Ticket 011 - Enhancement 2 Deployment

Classification: ACTUAL MINIKUBE LAB
Timestamp UTC: 2026-11-03T18:08:38.5381739+00:00

Helm release: ticket011-falco
Namespace: ticket-011-monitoring
Chart: falco-9.1.0
Starting revision: 2
Verified revision: 3

## Deployed Rules

- Ticket011 Unexpected Shell In Reporting Image
- Ticket011 Reporting ServiceAccount Token Access Attempt

Enhancement 1 SHA256: 12E024B3D1F4AD50FCE44D11731858559E90C82BE5C8B0F71724932662CC1CE0
Enhancement 2 V2 SHA256: 10192AE7CF4DBBC833D9AB0C4F355DFA415F94BE6D4BB73CD9320EA76ED21A5F
Values SHA256: E501A632B780F3468B5398FDC0B83719D0E2E5E8AC07B1F081A16F909E6B02CE

## Verified Outcomes

- Offline validation: PASS_NO_WARNINGS
- Helm upgrade exit code: 0
- Both custom rules in ConfigMap: VERIFIED
- Falco DaemonSet: 1/1 READY
- Ticket 010 namespace UID: UNCHANGED
- Reporting API UID/generation: UNCHANGED
- Reporting API availability: 1/1

## Pending Validation

- Confirm Enhancement 2 loads in Falco
- Positive test: failed open of absent token path
- Negative test: benign Python health check

No ServiceAccount token was accessed by this deployment.
No AWS or production environment was modified.