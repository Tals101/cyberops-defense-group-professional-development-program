# Ticket #009 — V2 Dry-Run Validation

## Objective

Validate that V2 can evaluate the same identity population without modifying identity state.

## Input Integrity

SHA256 before V2 dry run:

A90C324B953030B2C933CACC9FC104A2F5A29A15F6B02E1AB1420091640182D3

SHA256 after V2 dry run:

A90C324B953030B2C933CACC9FC104A2F5A29A15F6B02E1AB1420091640182D3

The hashes are identical.

This demonstrates that V2 dry-run mode generated decisions and evidence without modifying the original identity dataset.

---

# Decision Results

## AUTO_REMEDIATE

### nora.hayes

Recommendation: DISABLE

Reason:

- employee identity;
- lifecycle state inactive;
- interactive activity stale;
- evidence current and complete;
- standard privilege;
- no service dependency.

### kevin.brooks

Recommendation: DISABLE

Reason:

- workforce status terminated;
- evidence current and complete;
- standard privilege;
- no service dependency.

This corrects a significant V1 weakness.

V1 left this terminated employee enabled because it considered only interactive-login age.

### contractor.mills

Recommendation: DISABLE

Reason:

- contractor engagement expired;
- evidence current and complete;
- standard privilege;
- no service dependency.

---

# REQUIRE_APPROVAL

### admin.ops

Recommendation: REVIEW

Reason:

- privileged identity.

V2 does not permit unattended privileged-account disablement.

### svc_finance_batch

Recommendation: KEEP_ENABLED

Reason:

- interactive activity is old;
- non-interactive authentication is current;
- account is a service identity;
- production dependencies exist.

The Finance service account that V1 incorrectly disabled is no longer classified as an unattended remediation candidate.

### svc_records_archive

Recommendation: REVIEW

Reason:

- service identity;
- activity appears infrequent;
- production dependency exists.

The account requires owner and dependency review rather than automatic disablement.

---

# DO_NOT_AUTOMATE

### analytics.temp

Recommendation: REVIEW

Reason:

- unknown identity type;
- conflicting evidence;
- recent non-interactive activity;
- service dependency exists.

Confidence: LOW

### ingest.bridge

Recommendation: REVIEW

Reason:

- unknown identity type;
- incomplete evidence;
- stale data;
- elevated privilege;
- service dependency exists.

Confidence: INSUFFICIENT

---

# Comparison With V1

V1 disabled:

- nora.hayes;
- svc_finance_batch;
- svc_records_archive;
- contractor.mills;
- analytics.temp.

V2 dry run recommends automatic disablement only for:

- nora.hayes;
- kevin.brooks;
- contractor.mills.

V2 does not automatically disable:

- service identities;
- privileged identities;
- identities with unknown type;
- identities with conflicting or incomplete evidence.

---

# Key Finding

V2 demonstrates a safer separation between:

- risk detection;
- evidence quality;
- decision confidence;
- remediation authority.

A rule match no longer automatically becomes a state change.

The dry run also demonstrates that safety improvements do not require disabling automation entirely.

V2 can still identify legitimate low-risk remediation candidates while withholding authority from higher-impact or uncertain cases.

---

# Dry-Run Validation Result

**PASS**

V2 produced decisions without changing identity state.

The Finance service identity was protected from the V1 failure mode.

The terminated workforce identity missed by V1 was correctly identified for remediation.

Unknown and ambiguous identities failed safely into review rather than enforcement.
