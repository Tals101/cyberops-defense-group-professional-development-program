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

---

## Issue B — 09:40 Escalation

### Question
Does the new email-attachment evidence justify containing HR-LT-44?

### Why does this question matter now?
The workstation remains online after a user opened an email attachment that caused Word to launch encoded PowerShell. PowerShell executed before EDR blocked a child process.

### Evidence Needed
- Email attachment origin
- Actual sender address and headers
- Word-to-PowerShell telemetry
- EDR prevention details
- Network activity from HR-LT-44

### Observed Evidence
The triggering Word document came from an email attachment received about ten minutes before the EDR alert. The display name appears to be a company executive, but the actual sending address is not yet validated. PowerShell executed before EDR blocked one child process. The workstation remains network-connected.

### Interpretation
The email-origin evidence increases concern for phishing or malicious-document activity. The earlier benign decoded command lowers concern about the specific command reviewed, but it does not establish that the entire email/document activity was benign.

### Confidence
Moderate.

### Decision Impact
Yes. Issue B should move back to the highest Security investigation priority and containment is now justified because the endpoint remains online and the execution originated from a suspicious email attachment.

### Next Step
Preserve email and endpoint evidence and isolate HR-LT-44 from the network using the least disruptive available containment method.

---

## Issue B — Network Activity

### Question
Did HR-LT-44 successfully communicate with the external destination after PowerShell execution?

### Why does this question matter now?
A successful connection after suspicious document execution could indicate command-and-control, payload retrieval, or data transfer.

### Evidence Needed
External-server connection records and endpoint timing.

### Observed Evidence
The controlled external server at 192.168.56.150:8088 recorded a successful HTTP GET for /status.txt and returned HTTP 200.

The lab server recorded the source as 192.168.56.1 because of the VirtualBox host-network path.

### Interpretation
Successful outbound communication to the controlled destination is confirmed. The content observed in this lab request was benign, but the connection itself supports the scenario's network-activity finding.

### Confidence
High that the connection succeeded. Low regarding the purpose of the scenario's original unknown communication.

### Decision Impact
Yes. Successful external communication following suspicious execution supports keeping Issue B at Priority 1 and strengthens the containment decision.

### Next Step
Evaluate persistence, credential-access indicators, data access, and whether activity extends beyond HR-LT-44.

---

## Issue B — Data Access

### Question
Is there evidence that PowerShell could access HR data on the workstation?

### Why does this question matter now?
If suspicious execution accessed HR files, potential confidentiality impact increases and HR/Privacy involvement may become necessary.

### Evidence Needed
Process telemetry showing PowerShell accessing a representative HR file.

### Observed Evidence
In the controlled lab, PowerShell successfully read HR_Compensation_Sample.csv. Windows Security Event ID 4688 recorded the PowerShell command used to access the file.

The observed test process was PowerShell launched from PowerShell, not the original Word-launched process.

### Interpretation
The lab demonstrates that the executing user context had access to HR data. It does not prove that the original suspicious Word/PowerShell activity accessed that data.

### Confidence
High that the lab PowerShell process could access the sample HR file. Low that the original suspicious activity accessed HR data.

### Decision Impact
Potential data exposure remains an important incident question, but current evidence does not establish data theft.

### Next Step
Check for evidence of lateral movement and then determine whether investigation scope should remain one workstation or expand to the environment.

---

## Issue B — Scope Question

### Am I investigating one workstation, or am I investigating an environment?

At this point, I am investigating one primary workstation: HR-LT-44.

The confirmed suspicious execution, outbound communication, and available endpoint evidence are tied to HR-LT-44. No current evidence establishes lateral movement, credential reuse, or related execution on another system.

### What Would Cause the Scope to Expand?

I would expand the investigation from one workstation to the broader environment if evidence shows:

- Another endpoint communicating with the same suspicious destination
- The same attachment, sender, hash, or process chain on another host
- Shared credential use across systems
- Lateral-movement activity
- Related authentication anomalies
- Similar persistence mechanisms
- Additional users receiving or opening the same email
- Evidence that HR-LT-44 accessed or modified remote systems

### Current Scope Decision

Maintain HR-LT-44 as the primary incident system while conducting targeted environment-wide searches for related indicators.

### Confidence

Moderate.

### Decision Impact

The investigation remains focused enough to avoid unnecessary disruption, but the threshold for expanding scope is low because successful external communication has already been confirmed.

---

## Issue B — HR-LT-51 Scope Follow-Up

### Question
Does HR-LT-51 represent a second compromised workstation within the same incident?

### Why does this question matter now?
A second compromised host would materially expand incident scope, increase containment requirements, and raise the possibility of a broader campaign.

### Evidence Needed
HR-LT-51 process activity, network context, EDR findings, persistence, credential-access indicators, and authentication activity.

### Observed Evidence
HR-LT-51 contacted the same external destination as HR-LT-44, but rapid triage found:
- No Word-to-PowerShell execution chain
- No EDR High Severity alert
- No persistence indicators
- No credential-access indicators
- No suspicious authentication activity
- A user-initiated web request consistent with the observed connection

### Interpretation
The shared destination justified investigation but does not establish a shared root cause. Current evidence does not support classifying HR-LT-51 as compromised.

### Confidence
Moderate to high.

### Decision Impact
Yes. Do not contain HR-LT-51 solely because of the shared destination. HR-LT-44 remains the confirmed primary incident system.

### Next Step
Continue targeted environment-wide IOC searching while shifting into incident coordination for confirmed Issue B activity on HR-LT-44.
