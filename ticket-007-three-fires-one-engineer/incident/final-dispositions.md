# Ticket #007 — Final Dispositions

## Issue A — Privileged Authentication

### Final Classification
Likely Benign / Operational Process Failure

### Evidence
- Source IP mapped to a newly provisioned administrator workstation.
- The sysadmin account owner confirmed the login.
- Observed privileged commands were consistent with routine maintenance.
- No malicious commands were identified.
- Maintenance was not entered on the SOC calendar.

### Confidence
High.

### Security Impact
No confirmed security compromise.

### Business Impact
Minimal direct impact. The undocumented maintenance created unnecessary SOC escalation and uncertainty.

### Actions Taken
Validated the source, reviewed privileged activity, preserved logs, and confirmed administrator ownership.

### Remaining Actions
Correct the maintenance notification/change-management gap.

### Owner
Infrastructure Operations.

### Closure Criteria
Administrator activity remains consistent with authorized maintenance and the process gap is assigned for remediation.

---

## Issue B — HR-LT-44 Suspicious Execution

### Final Classification
Confirmed Security Incident

### Evidence
- Suspicious email attachment preceded the alert.
- Executive display name did not establish sender authenticity.
- Microsoft Word launched encoded PowerShell.
- PowerShell executed before EDR blocked a child process.
- HR-LT-44 successfully communicated with an external destination with no established business relationship.
- No confirmed persistence, credential theft, or lateral movement was identified.
- HR-LT-51 contacted the same destination but did not show the same suspicious execution chain.

### Confidence
High that a security incident occurred on HR-LT-44.
Moderate confidence that confirmed scope is limited to HR-LT-44.

### Security Impact
Potential unauthorized code execution and external communication. Sensitive-data or credential exposure was not confirmed.

### Business Impact
HR-LT-44 requires containment, investigation, and remediation, disrupting one HR user's workstation availability.

### Actions Taken
Containment recommended, evidence preserved, endpoint and network activity investigated, environment scope reviewed, and additional engineering support delegated.

### Remaining Actions
Complete identity review, mail search, remediation, clean-state validation, and environment-wide IOC review.

### Owner
Security Incident Response with Endpoint, SOC, IAM, and Email Administration support.

### Closure Criteria
HR-LT-44 is remediated, environment searches are complete, identity activity is cleared or addressed, no additional compromised systems are identified, and incident evidence is preserved.

---

## Issue C — Internet-Facing Portal

### Final Classification
Operational Issue with Security Follow-Up

### Evidence
- Portal experienced intermittent HTTP 500 errors.
- Operations had recently deployed a configuration change.
- Errors returned toward baseline after rollback.
- Unusual web requests continued after service recovery.
- Available timing evidence did not show that the unusual requests caused the degradation.

### Confidence
Moderate to high that the service degradation was caused by the configuration change.

### Security Impact
No confirmed portal compromise. Continued unusual internet traffic requires routine security review.

### Business Impact
Temporary customer-facing service degradation and increased support activity.

### Actions Taken
Preserved relevant logs, compared unusual traffic with errors, advised Operations not to delay rollback, and continued lower-priority security review.

### Remaining Actions
Monitor unusual requests and investigate further if exploit indicators or abnormal application behavior appear.

### Owner
IT Operations for service stability; SOC for security monitoring.

### Closure Criteria
Portal remains stable after rollback and ongoing traffic review shows no evidence of successful exploitation.
