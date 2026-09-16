# Ticket #007 — Priority Decision #3

## 1 — Issue B: Suspicious Email / PowerShell

**Current Priority:** 1

**What Changed:** The Word document came from an email attachment using an executive display name. The actual sender is unvalidated. PowerShell executed before EDR blocked a child process, and HR-LT-44 remains online.

**Current Risk:** Possible phishing or malicious-document execution with potential continued network access.

**Immediate Owner:** Security.

**Next Action:** Contain HR-LT-44, preserve endpoint and email evidence, validate the sender, and review network activity.

**When I Will Reassess:** After containment and initial email/network review.

### Does This Justify Containment?
Yes. The combination of suspicious email origin, Word launching encoded PowerShell, incomplete prevention, and continued network connectivity justifies endpoint containment.

### Cost of Waiting
Possible additional command execution, credential theft, network communication, or lateral movement.

### Cost of Containment
Temporary loss of network access and productivity for one HR user.

### High-Decision-Value Evidence
- Full email headers and actual sender address
- Attachment hash and metadata
- EDR process tree
- Network connections from HR-LT-44
- Evidence of persistence or credential access

### Delegation
The SOC analyst can preserve the email, validate sender information, and collect EDR/network telemetry while I manage containment and triage.

---

## 2 — Issue C: Internet-Facing Portal

**Current Priority:** 2

**What Changed:** Customer-facing errors remain important, but Security has already advised that rollback should not be delayed.

**Current Risk:** Availability impact plus unresolved unusual traffic.

**Immediate Owner:** IT Operations for rollback; Security for traffic review.

**Next Action:** Operations proceeds with rollback and reports whether service stabilizes.

**When I Will Reassess:** Immediately if rollback fails or exploitation evidence appears.

---

## 3 — Issue A: Privileged Authentication

**Current Priority:** 3

**What Changed:** The session remains concerning, but the source maps to an authorized administrative host and observed privileged commands were non-destructive.

**Current Risk:** Residual possibility of unauthorized or harmful privileged activity.

**Immediate Owner:** Security monitoring.

**Next Action:** Preserve logs and monitor for destructive commands, persistence, or unauthorized changes.

**When I Will Reassess:** Immediately if harmful privileged activity appears.
