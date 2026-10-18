# Ticket #009 — Before/After Engineering Experience

## Purpose

Compare the engineering and operator experience before and after the redesign of the identity-remediation automation.

## Before — V1 Automation

### Workflow

1. Evaluate interactive-login inactivity.
2. Apply a fixed inactivity threshold.
3. Disable qualifying identities.
4. Record the action after execution.

### Engineering Experience

The V1 workflow was simple to implement but provided insufficient context for destructive decisions.

It did not adequately account for:

- Service-account identity types
- Noninteractive authentication
- Application dependencies
- Business criticality
- Conflicting identity records
- Evidence trustworthiness
- Approval boundaries

### Operational Consequence

A service identity supporting Finance LedgerBridge was disabled, causing application disruption.

Operators were forced into reactive incident response, dependency investigation, containment, and recovery.

The automation's apparent certainty exceeded the quality of its evidence.

## After — V2 Automation

### Improvements

V2 introduced stronger authority boundaries and execution safeguards.

These included:

- Confidence-based decisions
- Protected identity classifications
- Approval-gated actions
- Execution limits
- Dry-run evaluation
- Deferred remediation
- Structured decision records
- Rollback and recovery testing
- Emergency-stop and logging controls

### Engineering Experience

Engineers could examine proposed actions before execution and distinguish automatic authority from approval-required decisions.

Failures could be reproduced through isolated tests rather than discovered through business disruption.

### Remaining Limitation

V2 improved execution safety but did not fully establish whether corroborating identity evidence was authentic, current, and independently trustworthy.

## After — V3 Automation

### Improvements

V3 added:

- Primary and secondary evidence corroboration
- Explicit evidence-trust classifications
- Detection of contradictory identity context
- Secondary-source integrity verification
- Observation-timestamp freshness validation
- Fail-closed behavior for evidence and logging failures
- Adversarial testing of evidence and approval trust boundaries

An isolated A03 correction also demonstrated signed, transaction-bound, single-use approvals.

### Engineering Experience

Operators can distinguish:

- What the automation recommends
- How confident the decision is
- Whether the underlying evidence is trustworthy
- Whether human approval is required
- Whether execution was actually performed
- What action is required after a safety failure

For example, payroll.emergency receives REQUIRE_APPROVAL when primary identity data conflicts with the critical payroll integration context.

### Remaining Limitation

Canonical V3 remains a laboratory dry-run decision engine.

The isolated A03 approval correction is not yet integrated with production remediation enforcement.

Production credential separation, protected approval services, and operational readiness remain unverified.

## Before/After Comparison

| Area | Before: V1 | After: V2/V3 |
|---|---|---|
| Decision basis | Interactive inactivity | Identity context and corroborated evidence |
| Service dependencies | Insufficient protection | Explicit dependency and criticality checks |
| Approval authority | Inadequate boundaries | Approval-required classifications and isolated approval validation |
| Evidence trust | Assumed from input data | Integrity, conflict, and freshness checks |
| Execution | Unsafe destructive behavior demonstrated | Canonical V3 dry-run; controlled isolated execution tests |
| Failure handling | Reactive investigation | Tested fail-closed conditions and escalation |
| Auditability | Limited explanation of authority | Structured decisions, logs, and test evidence |
| Recovery | Incident-driven | Tested rollback, idempotency, and failure injection |
| Operator clarity | Action-centric | Recommendation, trust, authority, and outcome separated |

## Engineering Trade-offs

The redesigned automation requires more engineering effort.

Additional requirements include:

- Maintaining authoritative evidence sources
- Protecting integrity baselines
- Refreshing time-sensitive data
- Managing approvals and credentials
- Maintaining execution and audit records
- Testing rollback and operational failures

These requirements add complexity but reduce the risk of granting destructive authority based on misleading or incomplete evidence.

## Overall Assessment

V1 optimized for automated action without adequate safety boundaries.

V2 improved execution control.

V3 improved the evaluation of evidence trust and demonstrated further safeguards against adversarial inputs.

The result is a more explainable and testable engineering workflow, but not a production-ready unattended remediation service.

## Recommendation

Retain V3 for dry-run evaluation and recommendations.

Use appropriately controlled human-approved procedures for destructive identity changes until production-grade approval, credential, audit, and recovery controls are integrated and validated.

## Supporting Evidence

- analysis/root-cause-and-blast-radius.md
- analysis/v1-v2-automation-comparison.md
- analysis/soc-manager-production-recommendation.md
- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md
- analysis/v3-operator-experience-examples.md
