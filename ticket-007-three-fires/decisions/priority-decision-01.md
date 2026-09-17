# Ticket #007 — Priority Decision #1

## Scenario Time
09:00

## Ranking

1. Issue B — HR-LT-44 suspicious Word-to-PowerShell activity
2. Issue A — APP-PROD-02 unusual privileged SSH login
3. Issue C — Internet-facing portal errors and unusual requests

## Decision

Begin with Issue B.

## Rationale

Issue B presented the strongest combination of security concern, time sensitivity, and reversible response options.

Known evidence included:

- Microsoft Word launched encoded PowerShell.
- EDR generated a High Severity alert.
- A child process was reportedly blocked.
- The endpoint remained online.
- The purpose of the encoded command was not yet known.

Issue A involved successful privileged authentication from an unusual internal source, but authorization had not yet been established.

Issue C had customer-facing impact, but a recent configuration change provided a credible operational explanation and Operations could continue parallel validation.

## Immediate Actions

- Rapidly decode and assess the PowerShell command.
- Determine whether additional child processes executed.
- Delegate source-IP and authorization validation for Issue A.
- Have Operations preserve portal logs, correlate the recent change, and prepare rollback if necessary.

## Confidence
Moderate.

## Reassessment Trigger

Re-rank immediately if:

- Issue A shows active or malicious privileged activity.
- Issue B shows additional execution, persistence, network activity, or stronger benign evidence.
- Issue C service impact materially worsens or requires an immediate operational decision.
