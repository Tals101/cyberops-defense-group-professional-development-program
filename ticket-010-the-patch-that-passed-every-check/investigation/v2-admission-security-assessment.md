# Ticket 010 - V2 Admission Security Assessment

## Assessment Status

Status: Validated in isolated Minikube laboratory

Production approval: NOT GRANTED

The V2 implementation combines Kubernetes Pod Security Admission
(PSA) with a ValidatingAdmissionPolicy (VAP) that checks image
reference formats.

Testing demonstrated successful admission and rejection decisions
for the specific scenarios documented below.

## 1. Original Security Problem

The original ledger-api Deployment contained unsafe settings,
including privileged execution, root execution, and privilege
escalation.

Kubernetes accepted the original Deployment manifest despite
those unsafe settings.

The investigation demonstrated that successful API validation
or deployment-template acceptance does not prove that a workload
is secure.

## 2. Implemented V2 Controls

### Pod Security Admission

Namespace: ticket-010-lab

The namespace uses:

- enforce: restricted
- warn: restricted
- audit: restricted
- enforce-version: v1.35
- warn-version: v1.35
- audit-version: v1.35

Restricted enforcement was shown to reject unsafe Pod creation.

### Custom Image Admission Policy

Policy: ticket010-image-reference-policy

Binding: ticket010-image-reference-binding

Configuration:

- failurePolicy: Fail
- validationActions: Deny
- Binding restricted to ticket-010-lab
- Pods: CREATE and UPDATE
- pods/ephemeralcontainers: UPDATE

The custom CEL validation requires image references to use
the illustrative registry.example.local prefix and a
SHA-256 digest in the required format.

The policy checks regular, init, and ephemeral container
image references.

## 3. Confirmed Security Tests

### Unsafe Pod Rejection

An unsafe Pod was rejected under Restricted PSA.

Evidence:
evidence/v2-psa-unsafe-pod-rejection.txt

### Deployment Controller Enforcement

An unsafe Deployment resource was accepted, but its
ReplicaSet could not create unsafe Pods.

This demonstrates a distinction between admitting a
Deployment template and admitting its resulting Pods.

Evidence:
evidence/v2-replicaset-admission-test.txt

### Compliant Pod Acceptance

A security-compliant Pod passed server-side dry-run admission.

Evidence:
evidence/v2-psa-compliant-pod-test.txt

### Mutable Image Rejection

A mutable image reference was rejected by the custom
ValidatingAdmissionPolicy.

Evidence:
evidence/v2-mutable-image-policy-rejection.txt

### Approved Image Reference Acceptance

A synthetic image using the approved lab registry and
SHA-256 digest format passed admission.

Evidence:
evidence/v2-image-policy-compliant-test.txt

### Unapproved Registry Rejection

An image from example.invalid was rejected, despite
having a correctly formatted SHA-256 digest.

Evidence:
evidence/v2-unapproved-registry-rejection.txt

### Init Container Protection

A Pod with a compliant main container and an unapproved
init-container image was rejected.

The clean retest removed an unrelated duplicate-port warning.

Evidence:
evidence/v2-unapproved-init-clean-retest.txt

### Ephemeral Container Protection

An unapproved ephemeral-container image was rejected using
the pods/ephemeralcontainers API subresource.

An approved-format ephemeral-container image was accepted
through the same API path.

Temporary test Pods were deleted afterward.

Evidence:
evidence/v2-ephemeral-subresource-test-clean.txt
evidence/v2-ephemeral-positive-test.txt

## 4. Final Configuration Audit

The final configuration audit reported:

- 11 checks passed
- 0 checks failed
- Policy generation: 2
- Observed generation: 2
- No remaining Deployments, ReplicaSets, or Pods
  in ticket-010-lab

Evidence:
evidence/v2-final-admission-audit.txt

## 5. Remaining Security Limitations

### Image Authenticity

The current policy validates image reference syntax.

It does not prove that the referenced image exists,
has been signed, or came from a trusted build pipeline.

### Image Provenance

No deployment-time verification of build provenance,
trusted builder identity, or signed attestations has
been demonstrated.

### Vulnerability Enforcement

V2 admission does not independently evaluate image
vulnerabilities or enforce image vulnerability thresholds.

### Deployment Pipeline Integration

The laboratory admission controls are active in Minikube.

This does not establish that production release pipelines
must execute every required security check.

### Scope and Privileged Access

The custom admission binding is limited to ticket-010-lab.

Other namespaces are not protected by this binding.

Administrative changes, policy exemptions, and control
tampering require additional governance and authorization
controls.

### Controller Templates

The policy evaluates matching Pod admission requests.

Acceptance of a Deployment resource itself does not
establish that its future Pods will be admitted.

### Synthetic Registry and Digests

registry.example.local and the repeated-character digest
values are illustrative test fixtures.

They do not establish registry availability, image identity,
or cryptographic trust.

## 6. V2 Assessment Conclusion

V2 successfully demonstrated enforcement against unsafe
Pod security settings and disallowed image reference formats
in the tested Minikube namespace.

The admission tests covered normal containers, init
containers, and ephemeral containers.

The remaining trust, image provenance, vulnerability,
and release authorization requirements will be addressed
in the next supply-chain security phase.

V2 is validated for this laboratory exercise.

Production deployment approval remains withheld.
