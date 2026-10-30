# Ticket 010 - V1 Security Control Assessment

## Purpose

Evaluate the effectiveness and limitations of the V1
Kubernetes deployment security preflight.

This assessment is based on controlled synthetic lab
tests. It does not constitute production authorization.

## Implemented Controls

P01 - Block privileged containers.
P02 - Block privilege escalation.
P03 - Require non-root execution.
P04 - Require SHA-256 image reference formatting.
P05 - Require CPU and memory requests and limits.
P06 - Require restricted capabilities and seccomp.
P07 - Warn on writable root filesystem.

Additional controls:
- Fresh Trivy configuration scan per preflight execution.
- Explicit synthetic registry hostname allowlist.
- HIGH/CRITICAL severity guard for unmapped findings.
- Nonzero exits for known policy failures.
- Missing-manifest execution failure.

## Validation Evidence

1. Unsafe Deployment:
   BLOCK, exit code 1.

2. Hardened workload with unapproved registry:
   BLOCK, exit code 1.

3. Hardened workload with lab-allowlisted registry:
   Configuration preflight passed, exit code 0.

4. Privileged init container:
   BLOCK, exit code 1.

5. Missing manifest:
   ERROR, exit code 2.

6. Unmapped synthetic HIGH finding:
   Original policy returned exit code 0.
   Corrected policy returned exit code 1.

7. Post-correction integrated regression:
   Unsafe deployment blocked.
   Hardened synthetic configuration passed.

## Remaining Limitations

- V1 is a local configuration preflight, not yet proven
  to be an enforced CI/CD deployment gate.
- A successful V1 preflight does not prevent direct
  Kubernetes API submissions that bypass the pipeline.
- Synthetic image digests are format-tested, not
  verified against a trusted registry.
- Registry hostname allowlisting does not establish
  image authenticity, signature, or build provenance.
- Trivy KSV-0125 remains reported for the illustrative
  registry.example.local hostname.
- Unknown HIGH and CRITICAL findings are now blocked,
  but unmapped lower-severity findings require a
  documented disposition policy.
- Not all explicit P01-P07 requirements are independently
  validated against effective Kubernetes security settings.
- Ephemeral-container admission and update paths have
  not been independently tested.
- The current preflight does not independently enforce
  container-image vulnerability scan results.
- Trivy 0.70.0 reported a skipped policy module requiring
  version 0.72.0 or later.
- Logging and scanner failure handling require further
  hardening and negative-path testing.

## Security Conclusion

V1 demonstrates effective rejection of the tested
unsafe configurations and a corrected fail-open defect.

V1 is not sufficient as a standalone production
deployment security boundary.

## Recommended Next Phase

Implement V2 Kubernetes admission enforcement so
that unsafe workloads are rejected by the cluster
independently of CI/CD pipeline execution.

Preserve V1 scripts, test manifests, vulnerability
evidence, and before/after policy results.
