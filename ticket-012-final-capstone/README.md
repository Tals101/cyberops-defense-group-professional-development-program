# Ticket 012 — Final Capstone

**Technical investigation:** COMPLETE  
**Security remediation:** INCOMPLETE  
**Production recommendation:** **NO-GO**  
**Incident closure:** **NOT AUTHORIZED**

This project investigates a simulated Kubernetes incident involving suspicious outbound connections, workload identity, deployment changes, detection engineering, and recovery. All incident data and identities are synthetic. No production changes or actual compromise are claimed.

## Prerequisites

Windows PowerShell, Python 3 (standard library), `kubectl`, Minikube, and a local container build environment. Work only in an isolated, authorized lab. Run commands below from the project root unless otherwise stated.

## Project layout

- `01-Incident-Management/` — initial triage, incident timeline, decision log.
- `02-Laboratory/` — Python services, Dockerfiles, manifests, architecture and reproduction guide.
- `03-Detection-Engineering/` — V1 and V2 detectors, CLI, evaluation scripts, dataset, tests.
- `04-Adversarial-Validation/` — synthetic test runner, matrix and evidence.
- `05-Controls-and-Recovery/` — control validation, containment and recovery documentation.
- `06-Closure/` — engineering report, executive brief and explicit decision record.
- `07-Evidence/` — preserved evidence, hashes, test outputs and index.

## Exact automated test commands

    python .\03-Detection-Engineering\tests\test_correlation_detector.py
    python .\03-Detection-Engineering\tests\test_correlation_detector_v2.py
    python .\03-Detection-Engineering\tests\test_detector_cli.py

**Observed:** 31 V1 + 9 V2 + 11 CLI tests passed (51 total). A passing test suite does not establish production readiness.

## Detector CLI usage

    python .\03-Detection-Engineering\src\detector_cli.py --input .\03-Detection-Engineering\synthetic-data\labeled-correlation-scenarios.json --output .\07-Evidence\supporting-outputs\detector-cli-default-results.json
    python .\03-Detection-Engineering\src\detector_cli.py --input .\03-Detection-Engineering\synthetic-data\labeled-correlation-scenarios.json --output .\07-Evidence\supporting-outputs\detector-cli-custom-results.json --window-seconds 60

Input: JSON object with a `cases` array, a single case, or an array of cases. Each case contains `network_event` and optional `deployment_event`. Output: JSON containing detections, explanations, warnings and per-record errors. Default correlation window: 300 seconds. CLI exit behavior: `0` = all cases processed; `1` = input/output error or skipped malformed record; `2` = argument error. Claimed identity is not independently authenticated. A detection does not establish malicious intent.

## Comparative and adversarial tests

    python .\03-Detection-Engineering\src\compare_baselines.py
    python .\03-Detection-Engineering\src\compare_detectors_v2.py
    python .\04-Adversarial-Validation\run_adversarial_validation.py

These scripts may regenerate evidence outputs. Run and inspect them **before** recording the final SHA256 manifest.

## Lab setup, limitations and cleanup

See `02-Laboratory/reproduction.md` for exact baseline setup commands, synthetic secret creation, image builds, deployment checks and cleanup instructions. These instructions describe a proposed clean build and have not been independently rerun on a fresh cluster. The historical incident used a different application state than the secured baseline.

The tested bridge-based Minikube CNI did **not enforce** the deny-all egress NetworkPolicy. The application allowlist and disabled service-account-token automount passed their own narrower checks, but container-wide outbound isolation remains unresolved. Containment and rollback experiments were performed only against disposable lab workloads.

Original hashes: `07-Evidence/SHA256SUMS.txt`. Final inventory and manifest: `07-Evidence/final-evidence-inventory.csv` and `07-Evidence/final-evidence-sha256.csv`. Regenerate these after changes before creating the final ZIP. Historical documents may retain earlier planning status; the final decision document controls the current assessment.

## Evidence Integrity

The original evidence SHA256 ledger is preserved at:

07-Evidence/SHA256SUMS.txt

The final project inventory and SHA256 manifest are:

- 07-Evidence/final-evidence-inventory.csv
- 07-Evidence/final-evidence-sha256.csv

To regenerate the final integrity manifest:

    python .\07-Evidence\build_final_manifest.py

Regenerate the manifest after changing any project files
and before preparing the submission ZIP.

The final manifest records the hashes of project files
at the time of generation. It does not independently
prove that earlier evidence was never modified.

Preserve the original evidence ledger and document
any subsequent evidence changes.
