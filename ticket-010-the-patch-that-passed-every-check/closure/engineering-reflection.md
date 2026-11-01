# Ticket #010 - Engineering Reflection

## The Patch That Passed Every Check

### 1. Engineering Objective

This project examined why an unsafe ledger-api
deployment configuration could pass existing checks,
and what controls would be required to prevent a
similar release.

The investigation was conducted using a synthetic
application, local security tools, and an isolated
Kubernetes laboratory.

The goal was not merely to make a scanner report
pass. It was to evaluate which controls actually
prevented unsafe release or deployment behavior.

### 2. What the Investigation Demonstrated

The initial unsafe workload passed Kubernetes
server-side configuration validation.

That result demonstrated an important distinction:
successful Kubernetes schema validation does not
establish that a workload is secure.

The baseline included privileged execution,
root execution, privilege escalation, and a
mutable image reference.

Subsequent testing examined those risks at
multiple points in the release lifecycle.

The resulting engineering work was divided into
policy and pipeline controls, admission controls,
and artifact-integrity checks.

### 3. Lesson One - Detection Is Not Enforcement

One of the most important findings was the
difference between detecting an unsafe condition
and proving that the condition blocked a release.

A scanner may identify a privileged container,
an outdated package, or another policy violation.

A successful detection does not automatically
prove that a pipeline, admission controller,
or release process rejected the exact test artifact.

The consolidated adversarial matrix contains
13 scenarios, with 12 verified outcomes and
one remaining review item.

A02 remains unresolved because the evidence
does not independently establish that the exact
fixture was blocked by the release gate.

Future testing should preserve both the scanner
finding and the actual gate decision.

### 4. Lesson Two - Enforcement Scope Matters

Restricted Pod Security Admission and custom
Kubernetes admission checks provided opportunities
to prevent unsafe workload configurations.

However, an admission policy is meaningful only
within its configured scope.

Tests must account for namespace targeting,
resource types, and relevant subresource paths.

The later recovery rehearsal deliberately used
a separate namespace outside the original custom
image-reference policy binding.

That choice protected the original test controls,
but it also limited what the recovery rehearsal
could demonstrate about integrated enforcement.

The correct conclusion is that configuration
rollback was verified, not that the complete V2
admission chain was tested during recovery.

### 5. Lesson Three - Image Identity Must Be Verifiable

The project examined image references, integrity
controls, signing, signer trust, and release decisions.

The recovery rehearsal exposed an additional
image-identity limitation.

Docker Desktop and Minikube reported different
image IDs for the same local image tag.

The running Pod matched Minikube's image ID,
and that runtime identity remained unchanged
through the rollback.

However, these observations did not establish
an end-to-end provenance chain back to the
original Docker Desktop image.

A production release should use independently
verifiable immutable artifact references and
approved signing and provenance controls.

### 6. Lesson Four - Recovery Requires Direct Testing

Documenting a rollback procedure is not the
same as demonstrating it.

On November 1, 2026, an isolated laboratory
rehearsal began with a healthy Deployment
revision and an HTTP 200 health response.

An intentionally incorrect readiness-probe
port produced an unhealthy revision.

The new rollout failed while the existing
healthy Pod remained available.

An explicit Kubernetes rollout undo succeeded.

The original readiness configuration was restored,
the application returned HTTP 200, and a separate
verification confirmed the recovered state.

The temporary rollback namespace was then
deleted and cleanup was verified.

This established a successful laboratory
configuration rollback.

It did not establish image-version rollback,
database recovery, or production restoration.

### 7. Operational Lesson - Tools Have State

The rollback command generated a warning that
the last-applied-configuration annotation was
not updated.

This matters because a later kubectl apply
operation may reintroduce configuration from
an older declarative state.

Recovery procedures must therefore include
configuration reconciliation, not merely an
apparently successful rollback command.

The project also demonstrated the importance
of refusing destructive reruns when an output
file or Kubernetes resource already exists.

### 8. Evidence Preservation and Traceability

Historical investigation evidence was retained.

Updated assessments were accompanied by
preserved earlier versions.

The original engineering notebook was not
rewritten to make later work appear contemporaneous.

A supplemental notebook documented subsequent
engineering work and clearly identified
unrecorded session dates and work durations.

Evidence timestamps were not treated as
proof of actual hours worked.

This approach preserves the distinction
between observed results, later analysis,
and unresolved questions.

### 9. What I Would Improve Next Time

A stronger engineering process would include:

1. A session log maintained throughout the work.
2. Recorded start and stop times for actual work.
3. Test identifiers tied to exact fixture hashes.
4. Explicit gate exit codes for every negative case.
5. Immutable image identities across build and runtime.
6. Controlled production-equivalent trust verification.
7. Admission-path tests for all relevant workload types.
8. Rollback validation covering application versions.
9. Backup and data-restoration testing where applicable.
10. Configuration reconciliation after any rollback.

These improvements would make the findings easier
to reproduce and support stronger operational decisions.

### 10. Remaining Limitations

The final record continues to contain open issues.

- A02 release-gate verification remains incomplete.
- End-to-end image provenance is not established.
- The laboratory rollback did not change image versions.
- The rollback rehearsal was outside the original
  custom V2 image-reference policy binding.
- Production recovery and data restoration were not tested.
- Residual risk R06 remains OPEN.
- Actual historical work durations remain unrecorded.

These limitations should not be converted into
successful findings without new evidence.

### 11. Final Engineering Judgment

The project demonstrates meaningful improvements
in laboratory validation, release controls,
adversarial test coverage, and recovery testing.

The successful configuration rollback is an
important verified engineering outcome.

However, demonstrated laboratory controls and
successful recovery exercises are not sufficient
to authorize production deployment.

Production readiness: NOT ESTABLISHED.

The appropriate recommendation is to retain
the release hold until the unresolved controls,
provenance requirements, and recovery acceptance
criteria have been addressed.

## Supporting Records

- notebook/engineering-notebook.md
- notebook/engineering-notebook-supplement.md
- tests/adversarial-test-matrix.csv
- investigation/v1-security-control-assessment.md
- investigation/v2-admission-security-assessment.md
- investigation/v3-engineering-assessment.md
- recovery/recovery-and-rollback-assessment.md
- recovery/rollback-rehearsal-evidence.txt
- recovery/rollback-final-verification.txt
- recovery/rollback-cleanup-verification.txt
- operations/residual-risk-register.csv
