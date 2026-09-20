# Ticket #007 — Priority Decision #3

*09:40 reassessment after the HR-LT-44 email details arrive.*

## 1. Issue B — Contain and investigate

The Word file was received as an email attachment under an executive display name, but the real sender is not authenticated. PowerShell ran before EDR blocked a child process, and HR-LT-44 remains online. The earlier decoded command was harmless; that finding does not explain away the delivery method or the prevention gap.

**My decision:** Move B back to first priority and recommend network containment of HR-LT-44. Preserve the email, endpoint telemetry, and network records before remediation. The SOC analyst can handle sender validation and the supporting collection while I coordinate containment.

**Cost of waiting:** More execution or network activity, possible credential abuse, or lateral movement. These are potential outcomes, not observed ones.

**Cost of containment:** One HR employee temporarily loses workstation connectivity and may need IT support.

**Most useful next evidence:** Full headers and sender, attachment hash and metadata, EDR process tree, connection history, and checks for persistence or credential access.

**Reassess:** After containment and the first round of email and network findings.

## 2. Issue C — Let Operations restore service

The portal still matters to customers, but Security has already advised that rollback can proceed. Operations owns restoration; I will keep a separate watch on the unusual traffic. A failed rollback or proof of exploitation would bring C back for immediate review.

## 3. Issue A — Monitor rather than disrupt

The SSH source is an authorized administrative host and the privileged commands seen so far are non-destructive. I will retain the logs and watch for harmful activity while authorization is completed. Evidence of persistence, destructive change, or unauthorized use would change this call.
