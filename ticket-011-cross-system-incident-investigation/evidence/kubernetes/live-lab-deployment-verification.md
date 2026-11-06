# Ticket 011 - Live Reporting API Deployment Verification

Evidence classification: ACTUAL ISOLATED MINIKUBE LAB

Verification timestamp: 2026-11-02T20:15:39.9816333-05:00

Cluster context: minikube
Namespace: ticket-011-lab
Pod: reporting-api-598b9767f5-scfzw
Pod UID: f2c5a54d-7174-4f06-ab16-1c21df762003

Deployment: reporting-api
Desired replicas: 1
Available replicas: 1

Image: ticket011-reporting-api:lab-v1
Runtime image ID: docker://sha256:21b58b7e3c5fff749a35afbe59f2fa65631ecefd9d9dcc1a0f10e836b9c8446a

Manifest SHA256: 916A87DA38DE247842A0E0D872C20223251801748A833B545FD8BD9CD4BD3E2F

## Verified Security Configuration

- Restricted namespace Pod Security Admission
- Dedicated reporting-api ServiceAccount
- ServiceAccount token automount disabled
- Run as non-root UID/GID 10001
- Privileged mode disabled
- Privilege escalation disabled
- Read-only container root filesystem
- All Linux capabilities dropped
- RuntimeDefault seccomp profile
- Readiness and liveness HTTP health probes
- Service type ClusterIP

## Evidence

- kubernetes-lab/manifests/reporting-api-restricted.yaml
- evidence/kubernetes/live-lab-deployment.json
- evidence/kubernetes/live-lab-pod.json
- evidence/kubernetes/live-lab-service.json
- evidence/kubernetes/live-lab-serviceaccount.json

## Scope and Limitations

The Deployment and Pod were observed running and ready
in an isolated Minikube namespace.

ClusterIP limits the Kubernetes Service to internal
exposure; this is not proof of NetworkPolicy isolation.

Automated readiness and liveness probes are configured.
Independent HTTP response verification remains pending.

Falco detection and Kubernetes audit-log collection
have not yet been validated.

The Docker base image is not yet digest-pinned in the
source Dockerfile. Production readiness is not established.

No AWS credentials or production data were supplied.

Earlier synthetic Kubernetes event files remain separate
from actual live laboratory evidence.