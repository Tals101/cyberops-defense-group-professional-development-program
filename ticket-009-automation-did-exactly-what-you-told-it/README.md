# Ticket #009 — The Automation Did Exactly What You Told It

## Security Automation Engineering | Identity Remediation Incident

- **Project Type:** Incident Response, Identity Security, Automation Engineering
- **Environment:** Synthetic Python-Based IAM Laboratory
- **Engineering Status:** Laboratory Validation Completed
- **Production Decision:** NO-GO for Unattended Destructive Remediation

## Executive Summary

An automated identity-remediation job disabled a service account required by a Finance application.

The automation executed its programmed rule correctly. However, the rule relied on interactive-login inactivity without adequately considering identity classification, business dependencies, or the authority required to disable an account.

The resulting incident demonstrated a fundamental security engineering problem:

**Correct execution of an unsafe rule can still produce a serious security and operational failure.**

This project investigates the incident, reproduces the original failure, develops two successive redesigns, and tests their safety boundaries.

The portfolio preserves the original failed implementation, unsuccessful tests, engineering discoveries, corrective controls, and final recommendations.

## Incident Timeline

| Time | Event |
|---|---|
| 08:52 | Identity-remediation automation executed |
| 08:57 | Finance Operations experienced application failures |
| 09:07 | SOC assumed incident ownership |
| Investigation | IAM identified a disabled service account |

A synthetic reconstruction demonstrated the failure involving `svc_finance_batch`, which supported Finance LedgerBridge.

## Engineering Evolution

### V1 — Original Automation

The original rule disabled enabled identities with at least 90 days of interactive-login inactivity.

The laboratory reproduced an incorrect service-account disable and a subsequent Finance application-health failure.

**Finding:** Interactive inactivity did not establish that an account was unused.

**Disposition:** Unsafe.

### V2 — Authority and Execution Controls

V2 introduced:

- Identity-aware decision logic
- Automation authority classifications
- Approval boundaries
- Protected identity handling
- Bounded state changes
- Dry-run evaluation
- Audit controls
- Emergency-stop testing
- Prechange snapshots and rollback
- Persistent cross-run deferral

Repeated-run testing exposed a weakness that allowed a deferred action to occur during a subsequent execution.

The failure was preserved, corrected, and successfully retested.

**Finding:** Safe automation requires controls that remain effective across executions.

### V3 — Evidence Trust and Adversarial Testing

V3 added:

- Secondary-source corroboration
- Evidence-trust classification
- Conflict detection
- Source-integrity verification
- Independent freshness validation
- Fail-closed error handling

The `payroll.emergency` scenario demonstrated that high decision confidence must not override conflicting evidence of a critical business dependency.

Canonical V3 remains **dry-run only**.

## Testing Summary

| Test Group | Scope |
|---|---|
| V2 T01–T15 | Execution safeguards, approval, logging, rollback, emergency stop |
| F01–F10 | Failure injection and operational safety |
| A01 | Secondary evidence poisoning |
| A02 | Freshness metadata forgery |
| A03 | Approval forgery and replay |

Original failures and corrective results are preserved.

The A03 signed approval and replay-protection controls were validated in an isolated laboratory workflow. They are not integrated into production identity enforcement.

## Key Engineering Findings

1. Interactive-login inactivity is not proof of overall identity inactivity.
2. Detection and remediation authorization must remain separate.
3. Business dependencies must influence destructive-action decisions.
4. A per-run action limit does not necessarily provide a cross-run safety boundary.
5. Agreement between evidence sources does not prove source integrity.
6. A source's freshness label does not prove the observation is recent.
7. Approval must be authenticated, scoped, time-limited, and replay-resistant.
8. Rollback can fail and must have an escalation procedure.
9. Laboratory validation does not establish production readiness.
10. Destructive automation requires independently enforced least privilege.

## Repository Structure

| Directory | Contents |
|---|---|
| `incident/` | Incident response, timeline, root cause, blast radius, closure |
| `environment/` | Identity environment design and synthetic datasets |
| `v1/` | Original design, implementation, results, and failure evidence |
| `design/` | IAM recommendation, authority model, V2 design |
| `v2/` | V2 source, decisions, safety tests, and execution evidence |
| `v3/` | V3 source, failure injection, adversarial tests, and evidence |
| `testing/` | Consolidated engineering comparisons and validation |
| `security/` | Credentials, authority, safeguards, and failure modes |
| `operations/` | Operator experience, operations, change control, drift |
| `management/` | Production recommendation and decision brief |
| `scripts/` | Supporting Python utilities |
| `data/` | Synthetic failure and adversarial test fixtures |
| `evidence/` | Original laboratory evidence and logs |
| `automation/` | Original working implementation locations |
| `simulation/` | Original synthetic data and test working copies |
| `tests/` | Original test implementations and detailed findings |
| `analysis/` | Additional engineering and final-report materials |

The original `automation/`, `simulation/`, and `tests/` paths are retained to preserve the laboratory and its evidence. Portfolio directories also contain selected copies for easier review.

## Main Deliverables

- [Final Engineering Report (Markdown)](analysis/final-security-automation-engineering-report.md)
- [Final Security Automation Engineering Report (PDF)](Final_Security_Automation_Engineering_Report.pdf)
- [Engineering Notebook](engineering-notebook.md)
- [Lessons Learned — 30 Questions](lessons-learned.md)
- [V1/V2/V3 Comparison](testing/v1-v2-v3-comparison.md)
- [Failure-Injection Results](testing/failure-injection.md)
- [Adversarial Testing Results](testing/adversarial-testing.md)
- [Production Recommendation](management/production-recommendation.md)
- [Management Decision Brief](management/security-automation-decision-brief.md)

## Reproducing the Laboratory

The original laboratory uses Python scripts, JSON identity records, CSV outputs, and file-based test fixtures.

The original implementations and test scripts are retained in their historical directories.

Before rerunning a scenario, inspect its input and output paths, preserve existing evidence, and use isolated working copies.

Some tests intentionally reproduce unsafe behavior against synthetic identities.

Do not execute destructive test scenarios against real accounts or production IAM systems.

Historical test results should not be interpreted as current evidence freshness or execution authorization.

## Portfolio Integrity

This project preserves meaningful Git commits throughout the engineering process.

The original failures, test discoveries, control redesigns, and corrective validations remain part of the history.

The Git history was not rewritten to conceal unsuccessful tests.

All identities and application dependencies in the laboratory are synthetic.

Temporary Python caches and the local SQLite approval-consumption database are excluded from version control.

## Production Recommendation

**NO-GO for full unattended destructive production identity remediation.**

Continue:

- Read-only identity evidence collection
- Dry-run decision evaluation
- Security recommendations
- Human-reviewed and separately authorized remediation

Production authorization requires protected approval infrastructure, independently enforced least privilege, authoritative fresh evidence, tamper-resistant audit logging, integrated recovery testing, and formal change approval.

## Conclusion

Ticket #009 demonstrates the distinction between writing automation that performs a task correctly and engineering automation that can be trusted with production authority.

**The automation did exactly what it was told to do. The engineering challenge was determining what it should be allowed to do.**
