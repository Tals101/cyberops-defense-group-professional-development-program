# Ticket #009 — V1 Identity Remediation Design

## 1. Purpose

Document the original V1 identity-remediation automation that was used to reproduce the Finance LedgerBridge incident.

This is a historical design record. It describes the original implementation and its weaknesses, not an approved production design.

## 2. Original Objective

The automation was intended to reduce security exposure by identifying and disabling accounts considered inactive.

Its primary indicator was the number of days since an identity's last interactive login.

## 3. Original Decision Rule

V1 used the following logic:

If an identity is enabled and its interactive-login inactivity is at least 90 days, disable the identity.

The original rule did not adequately differentiate employee accounts from service identities.

## 4. Inputs

The simulation used synthetic identity records containing account status and interactive-login inactivity.

Additional identity attributes existed in the dataset but were not adequately incorporated into V1's destructive authorization decision.

## 5. Implementation

Original implementation:

automation/v1-remediator.py

Portfolio copy:

v1/src/v1-remediator.py

Synthetic input:

simulation/identities-original.json

The program evaluated identities and generated remediation decisions and execution evidence.

## 6. Original Execution Results

The V1 simulation disabled five identities.

One affected identity was:

svc_finance_batch

This account supported Finance LedgerBridge and Finance Settlement Processor.

Although the account had legitimate noninteractive authentication activity and active application dependencies, V1 disabled it.

The synthetic Finance health check subsequently reported:

APPLICATION_STATUS=FAILED

## 7. Design Weaknesses

### Identity Classification

V1 did not adequately distinguish employee identities from service accounts.

### Authentication Context

The rule treated interactive-login inactivity as evidence of overall account inactivity.

### Dependency Awareness

Known application dependencies did not prevent destructive remediation.

### Authorization

The remediation workflow had authority to execute changes without an independent approval boundary proportional to their impact.

### Recovery

The original implementation lacked sufficient prechange recovery and rollback safeguards.

## 8. False Positives and False Negatives

False positive:

svc_finance_batch was disabled despite supporting legitimate Finance application activity.

False negative:

kevin.brooks represented a terminated workforce identity that remained enabled because it did not meet the interactive inactivity threshold.

The original rule could therefore both disrupt legitimate services and fail to remediate unnecessary access.

## 9. Engineering Finding

The fundamental failure was not that V1 executed its programmed rule incorrectly.

The failure was that an insufficient decision rule possessed excessive destructive authority.

Interactive inactivity alone did not establish that an identity was unnecessary or safe to disable.

## 10. Historical Disposition

V1 was classified as unsafe for unattended destructive remediation.

The original implementation and its failure evidence were preserved.

V2 subsequently introduced identity-aware decision logic, bounded authority, approval requirements, and additional execution safeguards.

V3 later introduced stronger evidence-trust validation.

These improvements do not change the historical V1 findings.

## 11. Supporting Evidence

- v1/results/v1-decisions.csv
- v1/results/v1-remediation.log
- v1/evidence/v1-failure-observation.md
- v1/evidence/finance-application.log
- incident/root-cause-analysis.md
- incident/blast-radius-analysis.md

## Final V1 Assessment

**FAIL — UNSAFE FOR UNATTENDED DESTRUCTIVE REMEDIATION.**

The original failure remains preserved as part of the engineering investigation and portfolio history.
