# Ticket 011 - Live HTTP Validation

Evidence classification: ACTUAL MINIKUBE LAB

Verification timestamp: 2026-11-02T20:19:15.7721273-05:00

Context: minikube
Namespace: ticket-011-lab
Pod: reporting-api-598b9767f5-scfzw
Pod UID: f2c5a54d-7174-4f06-ab16-1c21df762003
Service: reporting-api

## Results

Pod loopback /health: PASS - HTTP 200

Pod loopback /report: PASS - HTTP 200

Kubernetes Service /health: PASS - HTTP 200

Kubernetes Service /report: PASS - HTTP 200

Kubernetes Service unknown route: PASS - HTTP 404

Total: 5 PASS, 0 FAIL.

## Network and Service Evidence

Service type: ClusterIP

Ready endpoint matches Pod IP: YES

Pod IP: 10.244.1.26

Requests used in-cluster HTTP and Kubernetes Service DNS.

No host ports were published.

## Evidence

- kubernetes-lab/tests/http_probe.py
- evidence/kubernetes/live-lab-http-results.json
- evidence/kubernetes/live-lab-http-container-logs.txt
- evidence/kubernetes/live-lab-service-endpoints.json

HTTP probe source SHA256: A5EC179651C30FE048852B0939C0A2FD2785CA26696388053A1AD5D0624FFB6B

## Limitations

These tests validate application and Service connectivity
from within the running laboratory Pod.

They do not establish external availability,
NetworkPolicy enforcement, or production readiness.

Falco runtime alerts have not been validated.
Kubernetes audit-log capture has not been established.

No real AWS credentials or financial records were used.