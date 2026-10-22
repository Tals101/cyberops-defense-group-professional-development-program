# Ticket #009 — Engineering Notebook

## Notebook Information

- Project: Identity Remediation Incident
- Investigation period: October 11–18, 2026
- Environment: Synthetic identity-remediation laboratory
- Repository: cyberops-defense-group-professional-development-program
- Production identity changes: None
- Current recommendation: NO-GO for unattended destructive remediation

## Record-Keeping Note

This notebook was reconstructed from the project's preserved scripts, logs, validation reports, and Git history.

It is a retrospective engineering record, not a claim that every entry was written contemporaneously.

Original evidence and failed tests remain preserved in the repository.

---

## Entry 01 — Incident Intake

### Observed Evidence

- 08:52 — Identity-remediation job executed.
- 08:57 — Finance Operations reported application failures.
- 09:07 — SOC assumed incident ownership.
- IAM identified a disabled service account.

### Engineering Assessment

The timing suggested a relationship between remediation and application disruption.

The initial investigation needed to establish causation rather than assume the automation was responsible solely because the events were close together.

### Immediate Priorities

1. Contain further remediation.
2. Restore affected service.
3. Preserve automation and identity evidence.
4. Determine the scope of account changes.
5. Examine why the automation possessed destructive authority.

### Evidence

- incident/incident-response-record.md
- incident/incident-timeline.md
- incident/containment-and-recovery-record.md

---

## Entry 02 — Identity Context Investigation

### Finding

Interactive-login inactivity alone is insufficient to establish that an identity is unused.

Service accounts may authenticate noninteractively while supporting important applications.

### Required Context

- Identity classification
- Workforce status
- Ownership
- Business purpose
- Interactive and noninteractive activity
- Privileges
- Service dependencies
- Approval status
- Lifecycle status
- Evidence freshness and completeness

### Engineering Decision

Remediation authority must depend on identity context rather than inactivity alone.

### Evidence

environment/identity-context-analysis.md

---

## Entry 03 — Synthetic Laboratory

### Implementation

Created synthetic identity records and an isolated application-health simulation.

The original dataset contained ten identities.

The V3 dataset later expanded to eleven identities, including payroll.emergency.

### Safety Boundary

The laboratory operates on JSON files rather than production IAM accounts.

Destructive behavior is reproduced only against synthetic working copies.

### Evidence

- simulation/identities-original.json
- simulation/v3-identities.json
- simulation/finance-health-check.py
- environment/identity-environment-design.md

---

## Entry 04 — V1 Incident Reproduction

### Implementation

automation/v1-remediator.py

### Observed Failure

The original inactivity-focused automation disabled an identity supporting Finance LedgerBridge.

The simulated application-health evidence demonstrated business disruption.

### Root Cause

The automation confused interactive inactivity with lack of business use.

Identity classification, noninteractive activity, service dependencies, and destructive authority were inadequately constrained.

### Evidence

- evidence/v1-decisions.csv
- evidence/v1-remediation.log
- evidence/v1-failure-observation.md
- incident/root-cause-analysis.md

### Git Checkpoint

59e5fb6 — preserve ticket 009 failed V1 identity remediation

---

## Entry 05 — IAM Allowlist Decision

### Alternative Considered

Permanently exclude sensitive service identities from automated inactivity remediation.

### Risks

- Stale exceptions
- Hidden ownership problems
- Unnecessary continued access
- Unmonitored compromised identities
- Expanding exclusion scope

### Engineering Recommendation

Use narrowly scoped, owner-verified, time-bound exceptions with periodic review.

Do not implement unrestricted permanent allowlisting.

### Evidence

design/iam-manager-response.md

---

## Entry 06 — V2 Authority Model

### Design Change

Separate remediation recommendations from permission to execute them.

Authority categories:

- AUTO_REMEDIATE
- REQUIRE_APPROVAL
- DO_NOT_AUTOMATE

### Safeguards

- Protected identity types
- Approval requirements
- Execution limits
- Dry-run evaluation
- Deferred operations
- Structured audit records
- Rollback capability

### Evidence

- design/automation-authority.md
- design/v2-design.md
- automation/v2-decision-engine.py
- automation/v2-config.json

---

## Entry 07 — V2 Enforcement Testing

### Tests

Validated enforcement decisions, rollback, malformed data handling, logging failures, and emergency-stop behavior.

### Significant Finding

Repeated execution exposed a cross-run safety weakness.

The original failed test was preserved before the corrective control was implemented.

### Correction

The subsequent implementation enforced the repeated-run safety boundary.

### Evidence

- tests/t12-repeated-execution-finding.md
- tests/t12-corrective-validation.md
- tests/t14-logging-failure-validation.md
- tests/t15-emergency-stop-validation.md
- evidence/v2-enforcement-results.csv

---

## Entry 08 — V3 Design Decision

### Remaining V2 Concern

Safer execution does not guarantee trustworthy evidence.

Two sources may agree because one source has been corrupted or because both contain outdated information.

### V3 Design

Evaluate:

1. Decision confidence
2. Evidence trust
3. Recommended action
4. Automation authority

### New Evidence Controls

- Primary and secondary corroboration
- Conflict detection
- Protected source-integrity checks
- Observation timestamp validation

### Evidence

- v3/v3-decision.md
- analysis/v3-design.md
- automation/v3-decision-engine.py

---

## Entry 09 — Payroll Identity Conflict

### Test Identity

payroll.emergency

### Primary Context

Appeared to be an inactive standard employee identity.

### Secondary Context

Identified an active critical payroll integration.

### Historical V3 Result

- Confidence: HIGH
- Evidence trust: CONFLICTING
- Recommendation: DISABLE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

### Engineering Conclusion

A confident recommendation does not override conflicting business evidence.

### Evidence

testing/bad-data-analysis.md

---

## Entry 10 — V3 Failure Injection

### Test Set

F01 through F10.

### F01

Missing primary attributes initially produced excessive confidence.

Correction: independently validate mandatory identity fields.

### F02

Corrupted input caused failure without sufficient structured observability.

Correction: record a fail-closed input or parsing failure.

### F03

Audit logging failure initially occurred after decision output had begun.

Correction: add an audit logging preflight before processing.

### F04–F10

Validated duplicate execution, interrupted runs, remediation failure, rollback failure, approval timeout, unsupported identity type, and missing secondary corroboration.

### Evidence

tests/v3-failure-injection-results.md

---

## Entry 11 — A01 Evidence Poisoning

### Attack

Alter secondary context so that misleading evidence appears corroborated.

### Initial Result

- Confidence: HIGH
- Trust: TRUSTED
- Authority: AUTO_REMEDIATE

### Finding

Source agreement did not establish source authenticity.

### Correction

Validate the SHA256 of secondary context against a protected integrity baseline before generating decisions.

### Retest

- Status: FAIL_CLOSED
- Failure: SECONDARY_SOURCE_INTEGRITY_FAILURE
- Decision records: 0
- Remediation performed: False

### Evidence

- tests/a01-secondary-evidence-poisoning-finding.md
- tests/a01-secondary-evidence-poisoning-corrective-validation.md

---

## Entry 12 — A02 Freshness Forgery

### Attack

Label old evidence dated January 1, 2025 as current.

### Initial Result

The evidence received TRUSTED status and AUTO_REMEDIATE authority.

### Correction

Require observed_at_utc and independently calculate observation age.

Maximum permitted age: 24 hours.

### Retest

- Trust: STALE
- Authority: REQUIRE_APPROVAL
- Actual action: NO_ACTION_DRY_RUN

### Additional Change

The trusted secondary dataset changed, requiring a controlled integrity-baseline rotation.

### Evidence

- tests/a02-freshness-metadata-forgery-finding.md
- tests/a02-freshness-metadata-forgery-corrective-validation.md

---

## Entry 13 — A03 Approval Forgery and Replay

### Original Attack

A locally asserted APPROVED value permitted synthetic remediation.

A generic approval reference was successfully reused for a second disable after the test identity state was restored.

### Correction

Implemented an isolated approval-validation workflow with:

- HMAC-SHA256 signature verification
- Unique approval ID
- Target and action binding
- Authorized approver check
- Expiration validation
- SQLite one-time-use ledger

### Corrective Results

- Valid signed approval accepted
- Reused approval rejected
- Tampered signature rejected
- Incorrect target rejected
- Incorrect action rejected
- Expired approval rejected
- Missing key blocked
- Unavailable ledger blocked

### Additional Finding

An initial action-binding implementation checked a fixed action rather than the actual requested operation.

That weakness was corrected and retested.

### Limitation

The approval implementation is isolated and not integrated with production identity enforcement.

### Evidence

- tests/a03-approval-forgery-replay-finding.md
- tests/a03-approval-forgery-replay-corrective-validation.md
- evidence/v3-a03-approval-consumption.csv

---

## Entry 14 — Operational Readiness

### Engineering Work

Developed:

- Operator experience examples
- Before/after engineering comparison
- Automation authority matrix
- Safeguard register
- Failure-mode register
- Automation change record
- Operations plan
- Drift analysis

### Current Drift Finding

Secondary evidence observations dated October 16, 2026 have exceeded the 24-hour freshness threshold.

Historical TRUSTED and AUTO_REMEDIATE decisions must not be represented as current authorization.

### Evidence

- operations/automation-operations-plan.md
- operations/automation-drift.md
- security/safeguard-register.md

---

## Entry 15 — Production Decision

### Question

Should the organization enable unattended destructive identity remediation?

### Assessment

No.

The laboratory has demonstrated significant improvements but has not integrated all controls into a production enforcement service.

### Outstanding Requirements

- Independent approval issuance
- Protected one-time-use authorization
- Production least-privilege credentials
- Authoritative evidence refresh
- Protected audit logging
- Integrated emergency stop
- End-to-end rollback and recovery testing
- Formal production authorization

### Recommendation

Continue dry-run analysis, recommendations, and separately authorized human-approved remediation.

### Evidence

- management/production-recommendation.md
- management/security-automation-decision-brief.md

---

## Key Engineering Lessons

1. Inactivity is not equivalent to lack of business use.
2. Evidence agreement does not prove evidence integrity.
3. Evidence labels do not prove freshness.
4. Recommendations and execution authority are different.
5. Approval must be authenticated, scoped, and single-use.
6. Failure handling must be observable and fail closed.
7. Recovery must be tested, not merely documented.
8. Historical passing tests do not establish permanent safety.
9. Least privilege requires platform enforcement.
10. Production authorization is separate from laboratory validation.

## Final Notebook Status

Investigation, laboratory redesign, failure injection, adversarial testing, and production recommendation have been documented.

Supporting evidence remains in the incident, analysis, automation, simulation, evidence, and tests directories.

Full unattended destructive remediation remains NOT APPROVED.
