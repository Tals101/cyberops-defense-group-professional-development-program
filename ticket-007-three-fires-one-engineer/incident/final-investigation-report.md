# Ticket #007 — Final Investigation / Incident Report

## Executive Summary

Ticket #007 required simultaneous triage of three competing issues under limited staffing.

Issue A involved unusual privileged SSH access to APP-PROD-02. Investigation ultimately confirmed authorized maintenance from a newly provisioned administrator workstation. The security concern was closed as likely benign, with follow-up required for the missed SOC maintenance notification.

Issue C involved customer-facing portal degradation and unusual web requests. Security found no evidence that the unusual requests caused the failures. Operations rolled back a recent configuration change and error rates rapidly returned toward baseline. Issue C was classified as an operational issue with security follow-up.

Issue B developed into the primary security incident. An HR user opened an email attachment that resulted in Microsoft Word launching encoded PowerShell. PowerShell executed before EDR blocked a child process, and HR-LT-44 subsequently communicated successfully with an external destination with no established business relationship.

HR-LT-44 became the confirmed primary incident system.

---

## Initial Access / Triggering Event

The triggering Word document was received as an email attachment approximately ten minutes before the EDR alert.

The message used the display name of a company executive, while sender authenticity had not initially been validated.

The lab investigation preserved simulated email evidence representing this phishing-style delivery path.

---

## Process Activity

Windows Security Event ID 4688 confirmed:

WINWORD.EXE -> powershell.exe -> EncodedCommand

The encoded PowerShell command reviewed during rapid triage created only a benign marker file.

Later evidence established that PowerShell itself executed before EDR blocked a child process.

No additional malicious child process was confirmed from the available evidence.

---

## User Context

HR-LT-44 represents an HR employee workstation.

The user context had access to simulated HR compensation information, increasing the potential confidentiality impact if malicious execution had accessed similar real information.

Controlled testing confirmed PowerShell could read representative HR data, but this did not prove that the original suspicious process accessed or exfiltrated HR information.

---

## Network Activity

HR-LT-44 successfully communicated with the controlled destination at 192.168.56.150:8088.

The connection confirmed the scenario condition that outbound communication occurred after suspicious execution.

The purpose and content of the scenario's original external communication remain unknown.

---

## Security-Control Response

EDR generated a High Severity alert and blocked one child process.

However, PowerShell executed before the block occurred.

This demonstrated that prevention of one child process did not prove prevention of the entire execution chain.

---

## Persistence

Scheduled-task and common Windows Run-key checks found no evidence supporting persistence.

This finding is limited to the persistence mechanisms examined.

---

## Credential Access

No evidence supporting common credential-access tooling was identified in the available process telemetry.

Available historical logging was incomplete, so credential theft cannot be ruled out solely from the absence of matching events.

---

## Lateral Movement

No evidence supporting common lateral-movement tools or techniques was identified for HR-LT-44.

The available telemetry was limited.

HR-LT-51 later contacted the same external destination, but delegated triage found no matching Word-to-PowerShell chain, persistence, credential-access indicators, or suspicious authentication activity.

The shared destination alone did not establish lateral movement or a shared compromise.

---

## Data Access

Controlled testing demonstrated that PowerShell running in the lab user context could access simulated HR compensation data.

No evidence confirmed that the original suspicious Word/PowerShell execution accessed or transferred sensitive HR data.

---

## Scope

The confirmed incident scope is HR-LT-44.

HR-LT-51 was investigated because it contacted the same destination, but current evidence does not support classifying it as compromised.

Targeted environment-wide searches remain appropriate because another system contacted the shared destination.

---

## Containment and Response

Immediate containment of HR-LT-44 was recommended because:

- The activity originated from a suspicious email attachment.
- Word launched encoded PowerShell.
- PowerShell executed before EDR prevention.
- The workstation remained online.
- Successful external communication occurred.

Evidence preservation, email review, identity review, network searching, and endpoint remediation were assigned through the Incident Action Plan.

---

## Issue A Disposition

**Classification:** Likely Benign / Operational Process Failure

The sysadmin owner confirmed the login, the source was an authorized administrator workstation, and available commands were consistent with routine maintenance.

The remaining issue is failure to record maintenance on the SOC calendar.

---

## Issue B Disposition

**Classification:** Confirmed Security Incident

HR-LT-44 experienced suspicious email-driven execution followed by successful external communication.

Persistence, credential theft, lateral movement, and sensitive-data theft were not confirmed.

---

## Issue C Disposition

**Classification:** Operational Issue with Security Follow-Up

Portal errors rapidly improved after rollback of the recent configuration change.

Unusual web requests continued, but available evidence did not establish them as the cause of the service degradation or show successful exploitation.

---

## Key Decision Lessons

The investigation demonstrated that priority must change when evidence changes.

High severity did not automatically determine priority.

Customer impact temporarily made Issue C the most urgent operational decision, while later email and network evidence made Issue B the highest organizational security risk.

Issue A also demonstrated the importance of stopping primary investigation once sufficient evidence supports a lower-risk disposition.

---

## Final Confidence

**Issue A:** High confidence in likely-benign disposition.

**Issue B:** High confidence that a security incident occurred on HR-LT-44; moderate confidence that confirmed scope is limited to that workstation.

**Issue C:** Moderate to high confidence that the service degradation resulted from the configuration change rather than the unusual requests.

---

## Closure Recommendation

Ticket #007 may move toward closure when:

- HR-LT-44 remediation and clean-state validation are complete.
- Environment-wide IOC searches are complete.
- Identity and email reviews are resolved.
- Issue A's maintenance-notification gap is assigned for correction.
- Portal stability is confirmed and continued web monitoring shows no successful exploitation.
- All technical evidence and incident documentation are preserved.
