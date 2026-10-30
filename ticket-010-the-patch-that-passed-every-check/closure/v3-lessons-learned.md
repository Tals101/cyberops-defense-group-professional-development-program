# Ticket #010 - V3 Lessons Learned

## 1. Deployment Acceptance Is Not Security Approval

A Kubernetes API accepting a manifest does not establish that its resulting workload is safe.

Security-sensitive configuration must be validated independently.

## 2. A Valid Signature Is Not a Safety Guarantee

The vulnerable baseline image passed cryptographic verification under an isolated test signer but was still blocked because Trivy identified 44 HIGH vulnerabilities.

Authenticity, authorization, and vulnerability compliance are separate decisions.

## 3. Trust Must Be Explicit

The original trusted public key correctly rejected signatures from the separate test-signing identity.

Public keys should be approved through controlled governance, not simply accepted because a signature exists.

## 4. Scan Results Depend on Database Quality

An otherwise clean image cannot be approved when the vulnerability database is unacceptably stale or its integrity metadata is invalid.

Database freshness is a release-control dependency.

## 5. Use Immutable Artifact Identity

Image tags may change.

The signature and vulnerability checks must evaluate the intended digest-pinned artifact rather than independently resolved mutable tags.

## 6. Security Gates Should Fail Closed

Unexpected scanner failures, missing verification material, invalid reports, and signature failures must block release authorization.

Operational errors should be distinguishable from confirmed vulnerability-policy failures.

## 7. Negative Tests Are Essential

The final regression included unsigned, unauthorized-signer, and signed-vulnerable cases.

These cases demonstrate that the gate rejects conditions which might otherwise lead to false confidence.

## 8. Laboratory Success Has Boundaries

The local registry uses loopback HTTP.

The cryptographic test used temporary signing identities and bypassed transparency-log verification.

A successful local gate does not replace production identity, provenance, CI/CD, admission, and runtime controls.

## 9. Preserve Reproducible Engineering Evidence

Scripts, SBOMs, scanner JSON, signature-verification records, immutable image references, and SHA-256 inventories should be retained together.

Evidence allows later review of what was tested and which controls actually enforced the decision.

## 10. Future Improvement

Integrate the tested controls into a production-like deployment pipeline, verify deployed image digests, and conduct controlled rollback testing before requesting production authorization.

## Final Lesson

A release is not secure merely because its patch built, deployed, scanned successfully, or carried a valid signature.

Independent controls must agree on the exact artifact before release authorization.
