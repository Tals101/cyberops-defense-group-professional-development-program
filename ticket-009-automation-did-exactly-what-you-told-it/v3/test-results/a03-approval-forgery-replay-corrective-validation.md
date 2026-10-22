# A03 — Approval Forgery and Replay Corrective Validation

## Objective
Validate controls preventing forged, modified, expired, mismatched, or reused approvals from authorizing identity remediation.

## Original Failure
The original remediation test trusted an unverified APPROVED value.

Observed failures:
- Forged approval disabled nora.hayes.
- Generic approval disabled payroll.emergency.
- The same generic approval reference was reused successfully after restoring the simulated identity.

Result: FAIL — Approval forgery and replay were possible.

## Corrective Controls Implemented
The isolated corrected A03 test now requires:

1. A structured approval artifact.
2. A unique approval ID.
3. A bound target identity.
4. A bound requested action.
5. An authorized approver identifier.
6. An approval validity window.
7. HMAC-SHA256 signature verification.
8. A SQLite approval-consumption ledger with unique approval IDs.
9. Fail-closed behavior when the signing key or ledger is unavailable.

## Corrective Test Results

| Test | Observed Result | Status |
|---|---|---|
| Valid signed approval | APR-A03-001 verified and reserved; nora.hayes disabled | PASS |
| Approval replay | Previously consumed approval blocked; nora.hayes remained enabled | PASS |
| Signature tampering | Approval signature verification failed | PASS |
| Identity mismatch | Approval target mismatch | PASS |
| Action mismatch, initial test | DISABLE approval incorrectly accepted for ENABLE | FAIL — CORRECTED |
| Action mismatch, retest | Approval action mismatch | PASS |
| Expired approval | Approval expired | PASS |
| Missing verification key | Approval verification key unavailable | PASS |
| Unavailable consumption ledger | Approval ledger unavailable | PASS |

## Approval Consumption Evidence
- Approval ID: APR-A03-001
- Identity: nora.hayes
- Action: DISABLE
- Number of consumption records: 1
- Evidence: evidence/v3-a03-approval-consumption.csv

## Remaining Production Limitations
These controls were implemented in an isolated lab test, not deployed to a production identity platform.

The lab uses a shared HMAC key. A production design must establish an approval authority independent of remediation execution, protect verification credentials, and prevent remediation operators from issuing their own approvals.

The SQLite ledger is local and not tamper-resistant. Production requires a durable, access-controlled approval-consumption service with appropriate concurrency and recovery guarantees.

Approval verification alone is not sufficient to authorize remediation. Identity context, business dependencies, execution safeguards, audit logging, and recovery controls must also pass.

## Conclusion
A03 corrective testing passed for the tested forgery, replay, expiration, identity-binding, action-binding, and failure-handling scenarios.

Full unattended destructive remediation remains prohibited pending production-grade control integration and authorization.
