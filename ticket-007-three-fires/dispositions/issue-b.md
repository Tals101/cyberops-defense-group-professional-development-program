# Issue B — HR-LT-44 Word-to-PowerShell Activity

**Disposition: Confirmed Security Incident in the exercise scenario**

## Why it remains an incident

The email attachment preceded Word starting encoded PowerShell. An executive-looking display name did not authenticate the sender. PowerShell executed before EDR blocked a child process, and HR-LT-44 subsequently reached an external destination with no established business purpose.

In the controlled lab, the encoded command wrote a harmless marker and the destination returned a harmless response. Those test details do not establish a malicious payload or exfiltration; the scenario's unexplained email-driven behavior and successful outbound communication support the incident decision.

HR-LT-51 later contacted the same destination. Its rapid review did not find the same process chain or other supporting compromise indicators, so I did not classify it as a second compromised workstation on the destination match alone.

## Confidence and impact

I have high confidence in the scenario incident classification for HR-LT-44 and moderate confidence that it is the only **confirmed** affected host. Persistence, credential theft, lateral movement, and sensitive-data transfer were not demonstrated. The immediate business cost is containment and restoration of one HR employee's workstation; potential confidentiality impact remains under review.

## Response and ownership

Security Incident Response leads, with SOC, Endpoint Support, IAM, Email Administration, Network Engineering, and HR supporting their assigned questions. I recommended containment, preserved the available evidence, investigated the execution and connection, and delegated the second-host check.

Identity and mail reviews, environment-wide indicator searching, data-impact assessment, endpoint remediation, and clean-state validation remain to be completed or verified by their owners.

**Closure condition:** HR-LT-44 has been remediated and validated; the identity, mail, and environment checks are resolved; any additional affected hosts have been addressed; and the evidence is retained.
