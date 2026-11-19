# Ticket 012 — Laboratory Reproduction Guide

## Scope and prerequisites

This is a **synthetic, local-only** lab. Use an authorized Minikube cluster, PowerShell, Python 3, `kubectl` and Minikube's image builder. Never run the historical incident manifests against production. These clean-install instructions have **not** been independently rerun on a new cluster; verify each command and image build on that environment.

## 1. Confirm isolated cluster context

    minikube status
    kubectl config current-context

Expected context: `minikube`. Stop if any other context is active.

## 2. Establish namespace and synthetic identity credential

    kubectl create namespace ticket-012-lab
    $labToken = python -c "import secrets; print(secrets.token_urlsafe(24))"
    kubectl -n ticket-012-lab create secret generic ticket012-lab-auth --from-literal="LAB_AUTH_TOKEN=$labToken"
    Remove-Variable labToken

If namespace or secret already exists, inspect it instead of blindly recreating. The credential must be synthetic, never a real company credential. The deployment manifests reference the `LAB_AUTH_TOKEN` key in `ticket012-lab-auth`.

## 3. Build local images (from project root)

    minikube image build -t ticket012-internal-service:lab-v1 -f .\02-Laboratory\Dockerfile.internal-service .\02-Laboratory
    minikube image build -t ticket012-unapproved-collector:lab-v1 -f .\02-Laboratory\Dockerfile.unapproved-collector .\02-Laboratory
    minikube image build -t ticket012-application-api:lab-v2 -f .\02-Laboratory\Dockerfile.application-api .\02-Laboratory

These image tags match the verified baseline. The historical incident used a different lab-v1 application state that these secured-baseline commands do not recreate.

## 4. Deploy verified baseline manifests

    kubectl apply -f .\02-Laboratory\manifests\internal-service-deployment.yaml
    kubectl apply -f .\02-Laboratory\manifests\internal-service-service.yaml
    kubectl apply -f .\02-Laboratory\manifests\unapproved-collector-deployment.yaml
    kubectl apply -f .\02-Laboratory\manifests\unapproved-collector-service.yaml
    kubectl apply -f .\02-Laboratory\manifests\application-api-serviceaccount.yaml
    kubectl apply -f .\02-Laboratory\manifests\application-api-identity-secured.yaml

## 5. Verify deployed objects and application health

    kubectl -n ticket-012-lab rollout status deployment/application-api
    kubectl -n ticket-012-lab rollout status deployment/internal-service
    kubectl -n ticket-012-lab rollout status deployment/unapproved-collector
    kubectl -n ticket-012-lab get deployments,services,serviceaccounts
    kubectl -n ticket-012-lab get pods -o wide

Expected baseline: `application-api`, `internal-service` and `unapproved-collector` each with one ready replica; application identity uses `ticket012-application-api` with token automount disabled.

## 6. Execute repeatable synthetic tests

    python .\03-Detection-Engineering\tests\test_correlation_detector.py
    python .\03-Detection-Engineering\tests\test_correlation_detector_v2.py
    python .\03-Detection-Engineering\tests\test_detector_cli.py
    python .\04-Adversarial-Validation\run_adversarial_validation.py

Preserve outputs before further changes. Detector inputs are synthetic, not production telemetry.

## 7. Incident reproduction and evidentiary limitations

Historic manifests include `application-api-deployment.yaml`, `application-api-incident.yaml`, `application-api-secured.yaml` and `application-api-identity-secured.yaml`. Historic collector/application log records and deployment differences are under `07-Evidence/supporting-outputs/`. Do **not** deploy the historic incident or negative-test manifests until the matching historic image is reconstructed in a separate disposable environment and a restore plan has been validated.

NetworkPolicy was configured but **not enforced** by the tested Minikube bridge CNI. An application-level allowlist is not container-wide isolation. The detector compares claimed identity metadata rather than independently authenticating the workload.

## 8. Safe cleanup

First record cluster state, preserve evidence, and verify the namespace has **only** disposable Ticket 012 resources. Cleanup, if explicitly authorized for this local lab:

    kubectl delete namespace ticket-012-lab

This is destructive; do not execute during normal verification or against production.
