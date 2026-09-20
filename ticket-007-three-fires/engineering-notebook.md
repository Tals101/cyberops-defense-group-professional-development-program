# Ticket #007 — Engineering Notebook

These entries follow the investigation as I worked it. Each decision reflects the evidence available at that stage; later discoveries are recorded in later entries rather than used to rewrite earlier judgments.

---

## Issue B — Decode the Word-launched command

**Question I needed to answer:** What did the encoded PowerShell actually run, and would its behavior justify isolating HR-LT-44 right away?

**Why it mattered:** Encoding is a useful alerting signal, but the command contents have to be examined before I can describe what happened. I needed the Word/PowerShell process event, encoded text, decoded text, and resulting artifact.

**What I observed:** Windows Security Event ID 4688 tied `WINWORD.EXE` to `powershell.exe` with an encoded command. Decoding the lab payload produced:

    Set-Content -Path "C:\ticket-007-lab\issue-b\hr-lt-44-marker.txt" -Value "Ticket 007 benign encoded PowerShell simulation"

The resulting marker contained that expected harmless text.

**Interpretation:** This command wrote a local text file. Its encoding alone did not make the specific lab payload malicious. That answer narrowed one concern; it did not validate the document, sender, or every action on the workstation.

**Confidence:** High about what this decoded command did.

**Decision effect:** I reduced B's immediate urgency rather than spend all available time on this one event.

**Next:** Look for other child processes or related activity.

---

## Issue B — Did PowerShell spawn anything else?

**Question:** Does the process tree extend beyond the encoded PowerShell event?

**Evidence sought:** Security Event ID 4688 records in the relevant window with creator process ID `0x311c`.

**What I found:** The search did not return matching process-creation events.

**Interpretation:** I had no evidence of an additional child process in the records checked. The result is limited by the time window and available logging; it is not proof that no other activity occurred.

**Confidence:** Moderate.

**Decision effect:** The absence of a corroborated child process made an interruption for a more time-sensitive issue defensible.

**Next:** Revisit B if another alert or new endpoint context changes the picture.

---

## Issue A — Examine the live privileged session

**Question:** What was `sysadmin` doing with privileged access on APP-PROD-02?

**Why now:** The session was still live. If it was unauthorized, waiting could allow production changes before we understood the activity.

**Evidence reviewed:** Sudo events and the active SSH session. The observed commands were:

    sudo whoami
    sudo touch /tmp/ticket007-privileged-marker
    sudo ls -ld /root

**Interpretation:** Root-level activity was confirmed, but these particular commands were not destructive and did not create persistence. I could not infer authorization from command harmlessness alone.

**Confidence:** High in the commands captured; low about anything outside the available record.

**Decision effect:** Switching from B to the live session was justified, but the commands alone did not warrant emergency account or server containment.

**Next:** Keep A under review and reassess when Operations raises the portal decision at 09:25.

---

## Issue C — 09:25 rollback question

**Question:** Do we have a security reason to prevent Operations from restoring the previous portal configuration?

**Why now:** Customers were experiencing errors and the service team needed a decision, not an indefinite security hold.

**What I checked:** A 20-request portal sample returned **16 HTTP 200** responses and **4 HTTP 500** responses. In the earlier access log, an HTTP 500 preceded the unusual requests in the captured sample. Operations had a recent configuration change and a rollback path.

**Interpretation:** The availability issue was real. I did not have evidence that the unusual requests produced the failures; a change-related regression remained plausible.

**Confidence:** Moderate at this point, before observing rollback results.

**Decision effect:** I treated C as the most urgent *operational decision* and advised Operations to preserve the evidence and proceed with known-good rollback. Security would continue the request review in parallel.

**Next:** Compare error rates after restoration and reopen the security question if exploitation evidence emerges.

---

## Issue B — 09:40 email escalation

**Question:** Does the attachment and EDR context change the containment call for HR-LT-44?

**Why now:** An HR employee opened a document delivered by email, Word launched encoded PowerShell, and the endpoint had stayed connected despite a blocked child process.

**Evidence available:** The scenario placed the email roughly ten minutes ahead of the alert. It used an executive display name; the sender address had not yet been authenticated. PowerShell ran before EDR's child-process block. The workstation remained online.

**Interpretation:** The delivery context was consistent with a phishing-style document, even though the specific command I decoded earlier was a benign lab marker. That command did not establish that the whole event was authorized or safe.

**Confidence:** Moderate about the suspected email-driven incident at 09:40.

**Decision effect:** B moved back to my highest security priority. I recommended HR-LT-44 network containment and preservation of the email and endpoint evidence.

**Next:** Preserve records, isolate using the least disruptive available method, and validate the sender and network activity.

---

## Issue B — Check the external connection

**Question:** Did the HR-LT-44 lab host successfully reach the destination under review?

**Why now:** A successful outbound connection after suspicious document execution could indicate follow-on activity, but the connection's contents and owning process must be understood before describing its purpose.

**Evidence:** The controlled server at `192.168.56.150:8088` logged an HTTP `GET /status.txt` and returned `200`. Because of the VirtualBox host-network path, it showed the Windows source as `192.168.56.1` rather than the scenario workstation name.

**Interpretation:** The lab connection succeeded and the response was harmless. This validates the connectivity component of the scenario; it does not prove that the original unknown communication carried a payload, commands, or HR data.

**Confidence:** High for a successful controlled connection; low about the purpose of the scenario's original traffic.

**Decision effect:** The external-communication finding strengthened the rationale for maintaining B at Priority 1 and pursuing the wider endpoint questions.

**Next:** Examine persistence, credential-access indicators, data access, and possible additional hosts.

---

## Issue B — Could PowerShell read HR files?

**Question:** What information was accessible in the user context represented by HR-LT-44?

**Why now:** HR data access would materially change the confidentiality and stakeholder implications if the suspicious process had actually used that access.

**Evidence:** In a separate controlled test, PowerShell read `HR_Compensation_Sample.csv`. Windows Security Event ID 4688 captured the command. The test PowerShell was launched from another PowerShell session, **not** from the original Word event.

**Interpretation:** The test demonstrated access to a representative HR file in that lab context. It did not link the original Word-to-PowerShell activity to that file and did not establish exfiltration.

**Confidence:** High about the test's file access; low that the original suspicious process accessed HR data.

**Decision effect:** Data exposure stayed on the incident action list as an unresolved question rather than becoming a reported finding.

**Next:** Review lateral-movement indicators, then make an explicit scope decision.

---

## Issue B — One workstation or broader environment?

At this point, HR-LT-44 is the one **confirmed primary incident system in the scenario**. The suspicious process chain and successful controlled connection relate to it. I have not established another host with matching execution, credential reuse, or lateral movement.

**What would widen the search:** Another system contacting the destination; the same sender, attachment, hash, or process chain; related logons; shared account misuse; suspicious remote execution; matching persistence; more recipients opening the message; or signs of HR-LT-44 reaching other systems.

**Scope decision:** Keep the main investigation on HR-LT-44 while running focused environment-wide checks for related indicators. An indicator hit should prompt validation, not automatic containment.

**Confidence:** Moderate because endpoint and enterprise visibility remain incomplete.

**Decision effect:** This approach protects investigative focus without treating a one-host hypothesis as a certainty.

---

## Issue B — HR-LT-51 changes the scope question

**Question:** Is the second HR workstation compromised through the same activity, or is the destination match unrelated?

**Why now:** A second affected endpoint would widen containment and could indicate a broader campaign. Failing to validate it would be as problematic as assuming it was compromised.

**Evidence returned by delegated triage:** HR-LT-51 contacted the destination, but the engineer found no matching Word-to-PowerShell chain, no High Severity EDR alert, no persistence or credential-access indicators, and no suspicious authentication. The observed connection was consistent with a user-initiated web request during controlled testing.

**Interpretation:** The common destination was a reason to investigate HR-LT-51, not enough to attribute the same root cause. Available findings do not support classifying that workstation as compromised.

**Confidence:** Moderate to high for the second-host disposition within the checks performed.

**Decision effect:** I did not recommend isolating HR-LT-51 solely for the shared destination. HR-LT-44 stayed the primary incident system.

**Next:** Continue targeted environment searches and move the confirmed scenario incident into coordinated containment, impact review, and remediation planning.
