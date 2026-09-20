# Ticket #007 — Priority Decision #1

**Scenario time: 09:00**

## My initial order

1. **B — HR-LT-44 Word-to-PowerShell activity**
2. **A — APP-PROD-02 privileged SSH login**
3. **C — Portal errors and unusual web requests**

## Why B receives my first investigation slot

Word launching encoded PowerShell is unusual enough to require quick context. EDR reported a High Severity event and a blocked child process, but HR-LT-44 remained connected and I did not know what the command did. I could obtain a high-value answer quickly by decoding it and checking the process tree. If isolation became necessary, the immediate disruption would be concentrated on one workstation.

A could have more serious consequences if the login proves unauthorized, because APP-PROD-02 is a production system. For now, though, I only have an unfamiliar source and a successful login, not proof of misuse. C already has customer impact, but Operations can investigate the recent configuration change and prepare restoration alongside my security work.

## First actions

- Decode B's command and look for follow-on process activity.
- Have the SOC analyst identify A's source and verify expected administration.
- Ask Operations to retain C's logs, correlate the change window, and be ready to roll back.

**Confidence:** Moderate. This is the best use of attention with the information available at 09:00, not a final incident classification.

**Reasons to reassess immediately:** A becomes actively harmful or unauthorized; B reveals new execution, network activity, persistence, or convincing benign context; or C needs an urgent service-restoration decision.
