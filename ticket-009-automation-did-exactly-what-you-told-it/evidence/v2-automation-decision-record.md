# Ticket #009 — V2 Automation Decision Record

## Purpose

This record allows another engineer or auditor to reconstruct each V2 identity decision without reading the Python source code.

Decision chain: **Identity → Evidence → Decision → Authority → Action → Result**

---

# 1. emma.reed

## Identity

- Identity: `emma.reed`
- Identity type: `employee`
- Workforce status: `active`
- Owner: `Emma Reed`
- Business purpose: `standard workforce access`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `1`
- Days since non-interactive authentication: ``
- Privilege: `standard`
- Service dependencies: ``
- Approval status: `not_required`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `NO_ACTION`
- Reason: No remediation condition matched.

## Authority

- Authority classification: `AUTO_REMEDIATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `NO_ACTION`
- Actual action: `NO_ACTION`
- Result: `RECOMMENDATION_NO_CHANGE`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 2. samir.patel

## Identity

- Identity: `samir.patel`
- Identity type: `employee`
- Workforce status: `active`
- Owner: `Samir Patel`
- Business purpose: `finance analyst workforce access`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `12`
- Days since non-interactive authentication: ``
- Privilege: `standard`
- Service dependencies: ``
- Approval status: `not_required`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `NO_ACTION`
- Reason: No remediation condition matched.

## Authority

- Authority classification: `AUTO_REMEDIATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `NO_ACTION`
- Actual action: `NO_ACTION`
- Result: `RECOMMENDATION_NO_CHANGE`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 3. nora.hayes

## Identity

- Identity: `nora.hayes`
- Identity type: `employee`
- Workforce status: `inactive`
- Owner: `Nora Hayes`
- Business purpose: `former operations role pending lifecycle review`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `135`
- Days since non-interactive authentication: ``
- Privilege: `standard`
- Service dependencies: ``
- Approval status: `not_required`
- Lifecycle state: `inactive`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `DISABLE`
- Reason: Inactive lifecycle state with interactive login age 135 days.

## Authority

- Authority classification: `AUTO_REMEDIATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `DISABLE`
- Actual action: `DISABLE`
- Result: `SUCCESS`

## Recovery

- Reversible: `YES`
- Recovery method: Restore enabled state from pre-change snapshot and validate dependent services.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 4. kevin.brooks

## Identity

- Identity: `kevin.brooks`
- Identity type: `employee`
- Workforce status: `terminated`
- Owner: `Kevin Brooks`
- Business purpose: `former workforce account`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `18`
- Days since non-interactive authentication: ``
- Privilege: `standard`
- Service dependencies: ``
- Approval status: `expired`
- Lifecycle state: `pending_disable`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `DISABLE`
- Reason: Workforce status is terminated.

## Authority

- Authority classification: `AUTO_REMEDIATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `DISABLE`
- Actual action: `DISABLE`
- Result: `SUCCESS`

## Recovery

- Reversible: `YES`
- Recovery method: Restore enabled state from pre-change snapshot and validate dependent services.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 5. admin.ops

## Identity

- Identity: `admin.ops`
- Identity type: `privileged`
- Workforce status: `not_applicable`
- Owner: `Infrastructure Operations`
- Business purpose: `authorized infrastructure administration`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `3`
- Days since non-interactive authentication: ``
- Privilege: `administrator`
- Service dependencies: `Infrastructure Management`
- Approval status: `approved`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `REVIEW`
- Reason: Privileged identity requires approval for remediation.

## Authority

- Authority classification: `REQUIRE_APPROVAL`
- Approval required: `YES`

## Proposed and Actual Action

- Proposed action: `REVIEW`
- Actual action: `STAGE_ONLY`
- Result: `APPROVAL_REQUIRED`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 6. svc_finance_batch

## Identity

- Identity: `svc_finance_batch`
- Identity type: `service_account`
- Workforce status: `not_applicable`
- Owner: `Finance Applications Team`
- Business purpose: `Finance posting and settlement integration`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `240`
- Days since non-interactive authentication: `0`
- Privilege: `application`
- Service dependencies: `Finance LedgerBridge; Finance Settlement Processor`
- Approval status: `approved`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `KEEP_ENABLED`
- Reason: Interactive login is stale, but recent non-interactive authentication indicates active service use.

## Authority

- Authority classification: `REQUIRE_APPROVAL`
- Approval required: `YES`

## Proposed and Actual Action

- Proposed action: `KEEP_ENABLED`
- Actual action: `NO_ACTION`
- Result: `RECOMMENDATION_NO_CHANGE`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 7. svc_records_archive

## Identity

- Identity: `svc_records_archive`
- Identity type: `service_account`
- Workforce status: `not_applicable`
- Owner: `Records Management`
- Business purpose: `quarterly records archival process`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `400`
- Days since non-interactive authentication: `76`
- Privilege: `application`
- Service dependencies: `Records Archive Job`
- Approval status: `approved`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `REVIEW`
- Reason: Service account appears stale and requires owner and dependency review before remediation.

## Authority

- Authority classification: `REQUIRE_APPROVAL`
- Approval required: `YES`

## Proposed and Actual Action

- Proposed action: `REVIEW`
- Actual action: `STAGE_ONLY`
- Result: `APPROVAL_REQUIRED`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 8. contractor.mills

## Identity

- Identity: `contractor.mills`
- Identity type: `contractor`
- Workforce status: `contractor_expired`
- Owner: `Marketing Operations`
- Business purpose: `expired campaign support engagement`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `160`
- Days since non-interactive authentication: ``
- Privilege: `standard`
- Service dependencies: ``
- Approval status: `expired`
- Lifecycle state: `active`
- Data freshness: `current`
- Evidence completeness: `complete`

## Decision

- Confidence: `HIGH`
- Decision: `DISABLE`
- Reason: Workforce status is contractor_expired.

## Authority

- Authority classification: `AUTO_REMEDIATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `DISABLE`
- Actual action: `STAGE_ONLY`
- Result: `RUN_LIMIT_REACHED`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 9. analytics.temp

## Identity

- Identity: `analytics.temp`
- Identity type: `unknown`
- Workforce status: `unknown`
- Owner: `unknown`
- Business purpose: `analytics processing - ownership unresolved`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: `105`
- Days since non-interactive authentication: `2`
- Privilege: `standard`
- Service dependencies: `Analytics Processing`
- Approval status: `pending_review`
- Lifecycle state: `active`
- Data freshness: `mixed`
- Evidence completeness: `conflicting`

## Decision

- Confidence: `LOW`
- Decision: `REVIEW`
- Reason: Identity type is unknown or unsupported. Confidence=LOW; unattended remediation not permitted.

## Authority

- Authority classification: `DO_NOT_AUTOMATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `REVIEW`
- Actual action: `NO_ACTION`
- Result: `AUTOMATION_PROHIBITED`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# 10. ingest.bridge

## Identity

- Identity: `ingest.bridge`
- Identity type: `unknown`
- Workforce status: `not_applicable`
- Owner: `Data Engineering`
- Business purpose: `legacy integration - purpose requires validation`
- Enabled before evaluation: `True`

## Evidence Considered

- Days since interactive login: ``
- Days since non-interactive authentication: ``
- Privilege: `elevated`
- Service dependencies: `Data Ingestion Pipeline`
- Approval status: `unknown`
- Lifecycle state: `active`
- Data freshness: `stale`
- Evidence completeness: `incomplete`

## Decision

- Confidence: `INSUFFICIENT`
- Decision: `REVIEW`
- Reason: Identity type is unknown or unsupported. Confidence=INSUFFICIENT; unattended remediation not permitted.

## Authority

- Authority classification: `DO_NOT_AUTOMATE`
- Approval required: `NO`

## Proposed and Actual Action

- Proposed action: `REVIEW`
- Actual action: `NO_ACTION`
- Result: `AUTOMATION_PROHIBITED`

## Recovery

- Reversible: `YES`
- Recovery method: No production state change occurred; no rollback required.

## Evidence Sources

simulation/identities-original.json; evidence/v2-dry-run-decisions.csv; evidence/v2-enforcement-results.csv

---

# Auditor Review

## Could an auditor understand why an account changed without reading the Python source code?

**Yes.**

For every evaluated identity, the record contains the identity context, evidence considered, confidence, decision rationale, authority boundary, proposed action, actual action, result, and recovery method.

The decision record therefore provides an evidence trail independent of the implementation source code.

The CSV version is retained for structured analysis, while this Markdown version provides human-readable audit evidence.
