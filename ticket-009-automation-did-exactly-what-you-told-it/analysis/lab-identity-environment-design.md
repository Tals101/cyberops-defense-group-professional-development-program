# Ticket #009 — Lab and Identity Environment Design

## 1. Purpose

Document the synthetic identity environment used to reproduce the original remediation incident, evaluate V1, redesign V2, and validate V3 security controls.

## 2. Environment Classification

- Environment: Local cybersecurity laboratory
- Identity records: Synthetic
- Production identity platform: Not connected
- Production account changes: None
- Canonical V3 execution: DRY_RUN_ONLY
- Unattended destructive production execution: NOT APPROVED

## 3. Laboratory Architecture

The laboratory consists of five logical components:

1. Synthetic identity inventory
2. Identity-remediation decision engine
3. Execution and rollback simulation
4. Evidence and audit collection
5. Security validation and adversarial testing

Logical workflow:

Synthetic identity records
        |
        v
Primary IAM context ---- Secondary application context
        |                         |
        +-----------+-------------+
                    |
                    v
         Evidence validation
                    |
                    v
       Decision confidence and
       evidence-trust evaluation
                    |
                    v
       Automation authority decision
                    |
                    v
         Dry-run decision records
                    |
                    v
       Operator review and analysis

Separate isolated test workflows simulate approved remediation, failures, idempotency, and rollback.

## 4. Synthetic Identity Inventory

The original laboratory contains ten synthetic identities.

V3 expands the primary dataset to eleven identities, including payroll.emergency.

Identity attributes include:

- Username
- Identity type
- Workforce status
- Identity owner
- Business purpose
- Interactive-login inactivity
- Noninteractive authentication activity
- Privilege
- Service dependencies
- Approval status
- Lifecycle state
- Data freshness
- Evidence completeness
- Enabled state

Primary identity dataset:

simulation/v3-identities.json

## 5. Secondary Evidence

V3 uses a separate synthetic secondary identity-context dataset:

simulation/v3-secondary-context.json

The secondary records provide additional information concerning:

- Authoritative identity role
- Application dependencies
- Business criticality
- Registered ownership
- Expected authentication behavior
- Lifecycle status
- Source freshness
- Source confidence
- Observation timestamp

The purpose is to challenge misleading or incomplete primary IAM evidence rather than blindly corroborate it.

## 6. Business Dependency Simulation

The original incident involved an identity supporting Finance LedgerBridge.

The laboratory includes a synthetic application-health check and supporting log evidence to demonstrate the consequences of disabling a service identity.

The payroll.emergency scenario provides an additional example of a critical business dependency that conflicts with misleading primary identity context.

These are laboratory scenarios, not production application connections.

## 7. Automation Versions

### V1 — Original Remediation

Implementation:

automation/v1-remediator.py

The original logic primarily used interactive-login inactivity.

The simulation reproduced an unsafe disable affecting a business dependency.

### V2 — Authority and Execution Safeguards

Implementations:

- automation/v2-decision-engine.py
- automation/v2-enforcer.py
- automation/v2-rollback.py
- automation/v2-config.json

V2 introduced identity-aware decisions, approval boundaries, execution limits, dry-run capabilities, rollback, and additional safety checks.

### V3 — Evidence Trust

Implementations:

- automation/v3-decision-engine.py
- automation/v3-rollback.py
- automation/v3-source-integrity-baseline.json

V3 evaluates both decision confidence and evidence trust.

Additional controls include source integrity, observation-timestamp freshness, and fail-closed error handling.

Canonical V3 performs dry-run decision evaluation rather than production remediation.

## 8. Trust Boundaries

The laboratory evaluates four important security boundaries.

### Identity Evidence Boundary

Primary IAM information may be incomplete or misleading.

Secondary context must be independently evaluated.

### Source Integrity Boundary

A source cannot establish its own trustworthiness merely by agreeing with another source.

Protected integrity metadata is required.

### Freshness Boundary

A source-provided current label does not establish that the underlying observation is recent.

V3 applies a 24-hour secondary evidence freshness threshold.

### Approval Boundary

A remediation recommendation or locally asserted APPROVED value does not establish execution authorization.

The isolated A03 tests demonstrate signed, identity-bound, action-bound, expiring, single-use approval controls.

Those controls are not yet integrated into a production enforcement service.

## 9. Execution and Recovery Testing

Isolated laboratory tests cover:

- Duplicate execution
- Interrupted execution
- Failed remediation
- Failed rollback
- Approval timeout
- Unsupported identity types
- Missing evidence
- Approval forgery and replay

Working copies are used to prevent modification of the canonical synthetic identity inventory during destructive-action simulations.

## 10. Evidence Organization

The repository uses these directories:

- incident/ — Incident response and closure records
- analysis/ — Engineering assessment and recommendations
- automation/ — Decision engines, configuration, and rollback scripts
- simulation/ — Synthetic identity data and working copies
- evidence/ — Logs, decisions, and test outputs
- tests/ — Test implementations, findings, and validation reports

## 11. Laboratory Limitations

This environment does not establish:

- Real IAM platform integration
- Production least-privilege enforcement
- Independently hosted approval infrastructure
- Tamper-resistant production logging
- Protected production recovery access
- End-to-end production operational readiness

Historical evidence results are also subject to freshness drift.

## 12. Safety and Production Status

All destructive testing is limited to synthetic identity data.

No laboratory AUTO_REMEDIATE classification independently authorizes a real identity change.

The recommended production posture remains read-only evidence collection, dry-run evaluation, recommendations, and separately authorized human-approved remediation.

## Conclusion

The laboratory provides a controlled environment for investigating unsafe identity remediation and validating improvements to decision quality, automation authority, evidence trust, and recovery.

It demonstrates security engineering principles without granting production destructive authority.
