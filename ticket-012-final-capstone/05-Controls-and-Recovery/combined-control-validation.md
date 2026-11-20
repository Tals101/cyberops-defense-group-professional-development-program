# Ticket 012 - Combined Security Control Validation

## Objective
Validate two complementary security improvements
without disrupting authorized application functionality.

## Control 1 - Application Destination Allowlist
Application image: ticket012-application-api:lab-v2

Approved destination:
http://internal-service:8080/resource

Negative test result: PASS
Unapproved destination rejected with HTTP 403.
Security rejection event recorded.

Evidence reference: E018

## Control 2 - Kubernetes Workload Identity Protection
ServiceAccount: ticket012-application-api
Automatic token mounting: disabled

Validation result: PASS
Observed: TOKEN_PRESENT=False

## Combined Functional Validation
Application endpoint: /call-internal

Expected response:
{"result": "authorized", "data": "synthetic"}

Observed response:
{"result": "authorized", "data": "synthetic"}

Result: PASS

## Security Assessment
Both controls are implemented and tested.

The destination allowlist protects the application's
normal internal request path.

The workload identity control reduces unnecessary
Kubernetes API credential exposure.

## Remaining Risks
- Direct network access to unapproved services is not blocked.
- Application-level validation can be bypassed by
  independent code executing inside the container.
- Kubernetes NetworkPolicy enforcement is unavailable
  in the current bridge-based laboratory configuration.
- Complete incident containment has not been demonstrated.

## Final Control Status
Application destination allowlist: PASS
Workload identity protection: PASS
Authorized application communication: PASS
Network-level containment: NOT VERIFIED
Incident closure: NOT AUTHORIZED
