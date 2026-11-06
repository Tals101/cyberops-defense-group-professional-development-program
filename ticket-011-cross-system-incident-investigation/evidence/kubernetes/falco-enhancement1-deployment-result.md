# Ticket 011 - Detection Enhancement 1 Deployment

Classification: ACTUAL MINIKUBE LAB

Timestamp UTC: 2026-11-03T17:43:46.9012006+00:00

Release: ticket011-falco
Namespace: ticket-011-monitoring
Chart: falco-9.1.0

Starting Helm revision: 1
Installed Helm revision: 2

Rule: Ticket011 Unexpected Shell In Reporting Image

Rule SHA256: 12E024B3D1F4AD50FCE44D11731858559E90C82BE5C8B0F71724932662CC1CE0
Values SHA256: FA64D9C83A650D420169141AD0133F6264B8A20AE21493468FCAEF4C34B68923

## Verified

- Falco 0.44.1 rule validation: PASS
- Helm upgrade: SUCCESS
- Custom rule ConfigMap: PRESENT
- Falco DaemonSet: 1/1 READY
- Ticket 010 namespace UID: UNCHANGED
- Reporting API Deployment UID: UNCHANGED
- Reporting API availability: 1/1

## Limitations

The custom rule is deployed, but detection
correctness has not yet been tested.

Next tests must verify that Falco loads the
rule and generates an alert from noninteractive
shell execution in the reporting container.

A matching negative control is also required.

An earlier Falco container exit code 255
remains unresolved.

No AWS or production resources were modified.