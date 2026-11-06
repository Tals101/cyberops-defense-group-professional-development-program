# Ticket 011 - Detection Enhancement 1

Classification: LOCAL RULE DESIGN AND HELM RENDER

Timestamp: 2026-11-02T20:57:30.0718363-05:00

## Detection Objective

Detect unexpected shell execution in the
Ticket 011 reporting API container image.

Rule name:
Ticket011 Unexpected Shell In Reporting Image

## Detection Logic

- Process execution events: execve and execveat
- Container process, not a host process
- Reporting image repository identification
- Shell names: sh, bash, dash, ash, zsh
- No terminal requirement

The image-based condition is intentionally narrower
than a cluster-wide shell-execution rule.

## Security and Privacy

- No production data is processed.
- Alert output excludes command arguments.
- Existing Falco Helm settings are preserved.
- No cluster-wide RBAC is added.

## Files

- detection-engineering/detection-rules/ticket011-reporting-shell.yaml
- kubernetes-lab/falco-review/falco-enhancement1-values.yaml
- kubernetes-lab/falco-review/falco-enhancement1-rendered.yaml

Rule SHA256: 12E024B3D1F4AD50FCE44D11731858559E90C82BE5C8B0F71724932662CC1CE0

Proposed Helm values SHA256: FA64D9C83A650D420169141AD0133F6264B8A20AE21493468FCAEF4C34B68923

## Test Plan

Positive: launch sh in reporting container without TTY.

Negative: execute direct Python health check without shell.

Verify Falco attributes any custom-rule alert to
the Ticket 011 reporting container.

## Limitations

Helm template rendering: PASS

Falco rule syntax validation: NOT YET PERFORMED
Rule deployment: NOT PERFORMED
Live positive test: NOT PERFORMED
Live negative test: NOT PERFORMED

Container image metadata availability at runtime
still requires validation.

A future Helm upgrade would restart Falco and
temporarily interrupt monitoring. This change
has not yet been authorized or executed by this step.