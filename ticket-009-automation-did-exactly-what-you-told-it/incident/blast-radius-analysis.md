# Ticket #009 — Blast-Radius Analysis

## 1. Purpose

Assess the impact of the original identity-remediation failure, identify which identities and business services were exposed, and explain how the redesigned automation limits potential damage.

## 2. Incident Context

The original remediation job executed at 08:52.

Finance Operations reported application failures at 08:57.

SOC assumed incident ownership at 09:07.

IAM subsequently identified a disabled service identity.

The investigation reproduced the unsafe behavior in a synthetic laboratory.

## 3. Observed Laboratory Impact

The V1 simulation disabled five identities using a rule based primarily on interactive-login inactivity of at least 90 days.

One disabled identity was:

svc_finance_batch

This service account supported:

- Finance LedgerBridge
- Finance Settlement Processor

The identity had legitimate business purpose, a known Finance owner, and current noninteractive authentication activity.

Despite this context, V1 disabled it.

The synthetic Finance health check subsequently reported:

APPLICATION_STATUS=FAILED

The laboratory therefore demonstrated an incorrect identity-state change and a resulting application-dependency failure.

## 4. False-Positive and False-Negative Exposure

### False Positive

svc_finance_batch was disabled even though it supported legitimate application activity.

### False Negative

kevin.brooks represented a terminated workforce identity that remained enabled because its interactive-login age did not satisfy the V1 threshold.

These findings demonstrate that the original decision rule could both disrupt legitimate business operations and fail to remove unnecessary access.

## 5. Potential Production Blast Radius

V1's potential blast radius extended to any enabled identity within the automation's writable scope that met its inactivity condition.

Possible consequences included:

- Disruption of dependent applications
- Loss of scheduled service-account authentication
- Interruption of financial or operational workflows
- Disabled legitimate workforce identities
- Increased incident-response and recovery workload
- Continued access for terminated identities that escaped the rule

These represent potential risks rather than verified production outcomes.

## 6. Evidence Limitations

The provided incident facts do not establish:

- The complete production list of affected identities
- Every application dependency
- The full number of impacted users
- The total duration of business disruption
- The full financial or operational cost
- The precise pre-08:52 state of every identity

The five disabled identities are an observed synthetic V1 result, not a verified production incident count.

## 7. V2 Blast-Radius Controls

V2 introduced:

- Identity-aware decisions
- Protected identity classifications
- Approval requirements
- Maximum state changes per run
- Persistent deferred-action handling
- Prechange snapshots
- Postchange validation
- Audit logging
- Emergency stop
- Rollback testing

An initial repeated-run weakness was discovered and corrected using a persistent deferral mechanism.

## 8. V3 Additional Risk Reduction

V3 introduced:

- Secondary evidence corroboration
- Conflicting-evidence detection
- Source-integrity validation
- Independent freshness checks
- Fail-closed processing

Failure-injection and adversarial testing challenged these boundaries.

Canonical V3 remains dry-run only.

The tested A03 approval controls are not integrated into production enforcement.

## 9. Residual Risks

Production blast-radius controls remain unverified without:

- Enforced least-privilege IAM permissions
- Independent approval verification
- Protected audit infrastructure
- Integrated stop and rollback procedures
- Verified application recovery
- Current authoritative identity evidence
- Formal production authorization

## 10. Final Assessment

The laboratory demonstrated that a single incorrectly disabled service identity could interrupt critical Finance application dependencies.

The full production blast radius remains unknown.

V2 and V3 reduced documented laboratory risks, but neither establishes authorization for unattended destructive production remediation.

**Disposition: NO-GO for unattended destructive production execution.**

## Supporting Evidence

- incident/root-cause-analysis.md
- incident/incident-timeline.md
- evidence/v1-decisions.csv
- evidence/finance-application.log
- tests/t12-corrective-validation.md
- tests/v3-failure-injection-results.md
- tests/v3-adversarial-test-results.md
