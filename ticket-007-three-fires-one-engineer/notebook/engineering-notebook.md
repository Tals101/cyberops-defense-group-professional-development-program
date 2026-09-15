# Ticket #007 — Engineering Notebook

## Phase 2 — Issue B Investigation

### Question
What exactly did the encoded PowerShell command do?

### Why does this question matter now?
If the command performed malicious actions, Issue B may still require immediate containment. If it was benign, attention may need to shift elsewhere.

### Evidence Needed
- Word-to-PowerShell process evidence
- Encoded command
- Safely decoded command
- Resulting files or actions

### Observed Evidence
Windows Event ID 4688 confirms WINWORD.EXE launched powershell.exe with an encoded command.

The decoded command was:

Set-Content -Path "C:\ticket-007-lab\issue-b\hr-lt-44-marker.txt" -Value "Ticket 007 benign encoded PowerShell simulation"

The resulting marker file contains the expected benign text.

### Interpretation
The encoded command only created a local text file. No malicious behavior is shown by this command.

### Confidence
High.

### Decision Impact
This lowers the urgency of Issue B. Based on this evidence alone, Issue B does not currently justify consuming all available investigation time.

### Next Step
Check whether there is evidence of additional PowerShell activity, network connections, persistence, or other child processes associated with the event.

---

## Issue B — Child Process Check

### Question
Did the encoded PowerShell process launch additional processes?

### Why does this question matter now?
Additional child processes could indicate that EDR blocked only part of a larger execution chain.

### Evidence Needed
Windows Security Event ID 4688 records showing process ID 0x311c as the creator process.

### Observed Evidence
No matching process-creation events were found during the relevant time window.

### Interpretation
There is currently no evidence that the encoded PowerShell process launched additional child processes.

### Confidence
Moderate.

### Decision Impact
This further lowers Issue B's immediate urgency and makes switching attention to a higher-risk interruption more defensible.

### Next Step
Reassess priority if new information arrives about another issue.

---

## Issue A — Active Privileged Session

### Question
What are the privileged commands being executed by sysadmin?

### Why does this question matter now?
The session is active on a production server. The nature of the commands determines whether immediate containment is justified.

### Evidence Needed
Sudo activity associated with the sysadmin session.

### Observed Evidence
The session executed:
- sudo whoami
- sudo touch /tmp/ticket007-privileged-marker
- sudo ls -ld /root

### Interpretation
The commands confirm active root-level activity, but none of the observed commands is destructive or establishes persistence.

### Confidence
High regarding the commands observed. Low regarding whether additional activity occurred outside this evidence.

### Decision Impact
Issue A deserved the priority switch because privileged activity was actively occurring. However, the commands observed so far do not justify emergency containment by themselves.

### Next Step
Keep the session under review and reassess all three issues when the 09:25 Operations escalation arrives.

---

## Issue C — 09:25 Operations Escalation

### Question
Does Security have evidence that malicious traffic is causing the portal errors?

### Why does this question matter now?
Customers are affected and Operations needs a rollback decision. Security should not delay restoration without evidence that rollback would create security risk or destroy critical evidence.

### Evidence Needed
Current HTTP error sample, unusual-request timing, and configuration-change information.

### Observed Evidence
A current sample of 20 normal portal requests produced 16 HTTP 200 responses and 4 HTTP 500 responses.

Earlier evidence showed a 500 error before the observed unusual requests.

Operations has a recent configuration change and a rollback is available.

### Interpretation
The portal has a real availability problem, but current evidence does not show that the unusual traffic is causing the failures. The configuration change remains a credible operational explanation.

### Confidence
Moderate.

### Decision Impact
Yes. Issue C now requires an immediate operational decision because customers are affected. Security does not currently have evidence that justifies delaying rollback.

### Next Step
Recommend that Operations preserve relevant logs and perform the known-good rollback while Security continues reviewing the unusual traffic.
