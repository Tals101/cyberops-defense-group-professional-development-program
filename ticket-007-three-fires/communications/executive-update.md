# Ticket #007 — Executive Update

## Situation

We investigated three issues at the same time: an unexpected privileged login, suspicious activity on an HR workstation, and a customer portal outage. The HR workstation, **HR-LT-44**, is the primary security incident in this exercise.

An HR employee opened an email attachment. Word then launched encoded PowerShell; PowerShell ran before EDR blocked a child process. The workstation later made a successful connection to a destination for which we have no established business purpose. The lab reproduced the sequence with harmless commands and a controlled server; the scenario's original external communication remains unexplained.

## What the evidence supports

- Suspicious email-driven execution occurred on HR-LT-44, followed by an external connection.
- EDR blocked a child process, but that block did not prevent the initial PowerShell execution.
- HR-LT-51 also contacted the destination. Its rapid review did **not** find the matching process chain or other evidence supporting compromise.
- We have not established persistence, credential theft, lateral movement, or the loss of employee information.

## Remaining questions

We still need to determine the purpose of the original outbound traffic, whether sensitive files or credentials were affected, whether the attachment reached other employees, and whether additional endpoints have related indicators.

## Business impact

One HR workstation needs containment and remediation, with some disruption to that employee's work. There is no confirmed sensitive-data loss at this point. Separately, the portal's errors improved after Operations reverted a configuration change. Security is continuing a lower-priority review of the unusual web traffic.

## Response in progress

Security is coordinating endpoint containment, preservation of email/Windows/EDR/network evidence, searches for related activity, an identity review, and the HR data-access assessment. Network Engineering and Email Administration support the searches; HR and Endpoint Support are involved for user impact and restoration.

## Management support and escalation

Please support the cross-team response and any broader containment decision if additional compromised hosts emerge. Legal/Privacy should be brought in if the evidence gives us a reasonable basis to suspect sensitive employee data exposure.

## Confidence and next update

I have high confidence in the suspicious execution and successful connection on HR-LT-44; moderate confidence that it is the only confirmed affected workstation; and low confidence about whether sensitive data or credentials were accessed. I will update management when the identity, email, data-access, or environment searches materially change the scope or impact.
