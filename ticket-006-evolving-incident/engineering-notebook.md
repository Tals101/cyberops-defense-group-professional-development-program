# Ticket #006 — Engineering Notebook

## Investigation Step 1 — Network Activity

### Question
What exactly is the outbound HTTPS activity associated with FIN-WS17?

### Evidence Needed
- Destination IP address
- Destination port and protocol
- Source IP address
- Connection timing
- Number of observed connections
- Network traffic characteristics

### Observed Evidence
Not yet examined.

### Interpretation
Pending evidence review.

### Confidence
Low

### Next Step
Review the preserved network packet capture to establish the basic connection facts before examining host processes or file activity.

### Step 1 Findings

#### Observed Evidence
The preserved packet capture shows two separate outbound TCP sessions from FIN-WS17 lab IP 192.168.56.121 to external destination 198.51.100.77 on TCP port 443.

- Connection 1 began at approximately 18:16:34 lab time.
- Connection 2 began at approximately 18:17:21 lab time.
- The connections occurred approximately 47 seconds apart.
- Both sessions exchanged application data.
- The second session contained more client-to-server encrypted payload than the first.

#### Interpretation
The packet capture confirms unusual outbound communication to the external destination over TCP/443, consistent with the original HTTPS alert. However, the network evidence alone does not identify the initiating process or determine whether either connection was legitimate or unauthorized.

#### Confidence
High confidence that two outbound TCP/443 sessions occurred.
Low confidence regarding their purpose or security significance.

#### Next Step
Identify which processes executed around the times of the two network connections and determine whether multiple processes could explain the activity.

## Investigation Step 2 — Process Correlation

### Question
Which processes correspond to the two outbound HTTPS connections?

### Evidence Needed
- Process execution records
- Command-line arguments
- Process timing
- Parent/child relationships
- User and effective-user context

### Observed Evidence
Audit process-execution telemetry shows:

1. At approximately 18:16:34, finance_sync.sh executed as effective user mreynolds.
2. finance_sync.sh launched curl to POST /home/mreynolds/Reports/daily_summary.txt to https://finance-sync.local/api/report.
3. At approximately 18:17:21, /home/mreynolds/.local/bin/document_cache.sh executed as effective user mreynolds.
4. document_cache.sh launched tar to create /tmp/finance-cache-mreynolds.tar.gz containing:
   - Q3_budget.csv
   - vendor_payments.csv
5. gzip compression occurred as part of the archive process.
6. curl then POSTed the temporary archive to https://finance-sync.local/api/cache.
7. The temporary archive was deleted immediately afterward with rm -f.

The audit records show uid/euid=mreynolds but auid=analyst due to the controlled lab execution method. Therefore, the evidence establishes execution in the mreynolds security context but does not establish that mreynolds personally initiated the commands.

### Interpretation
The first HTTPS connection has a plausible business explanation: finance_sync.sh transmitted a daily Finance summary.

The second connection is substantially more suspicious. It involved collecting two Finance data files into a temporary compressed archive, transmitting that archive over HTTPS, and deleting the temporary archive immediately afterward.

This sequence is consistent with possible data staging and exfiltration. However, authorization and business purpose have not yet been established, so compromise is not yet confirmed.

### Confidence
High confidence regarding the process sequence and correlation with the two HTTPS sessions.

Medium confidence that the second activity represents unauthorized data transfer.

### Next Step
Examine Finance file-access audit telemetry to independently confirm which Finance files were accessed during the suspicious process and correlate those events with the 18:17:21 activity.

## Investigation Step 3 — Finance File Access

### Question
Which Finance files were actually accessed during the suspicious process sequence?

### Evidence Needed
- File open events
- File paths
- Access mode
- Process responsible
- Event timing
- User context

### Observed Evidence
File-access audit telemetry shows:

1. At approximately 18:16:02, Q3_budget.csv was opened read-only by the cat process running as effective user mreynolds.
2. At approximately 18:17:21, the tar process associated with document_cache.sh accessed the Finance directory.
3. The same tar process then opened Q3_budget.csv read-only.
4. The tar process also opened vendor_payments.csv read-only.
5. These file accesses occurred at the same time as creation of the temporary Finance archive and immediately before the second HTTPS transfer.

### Interpretation
The first access to Q3_budget.csv is consistent with ordinary Finance user activity.

The later activity independently confirms that document_cache.sh caused both Finance files to be read during creation of the temporary compressed archive.

When correlated with the prior process evidence and network evidence, this supports a sequence of:
Finance file access -> archive creation -> HTTPS transfer -> archive deletion.

This pattern is consistent with data staging and possible exfiltration. Authorization has not yet been established.

### Confidence
High confidence that Q3_budget.csv and vendor_payments.csv were read by the archive process.

Medium-to-high confidence that the second HTTPS session was associated with staged Finance data.

### Next Step
Examine the external HTTPS server request log to determine what requests were received, their order, and the amount of data submitted, without yet examining the contents of the received data.

## Investigation Step 4 — External Server Request Correlation

### Question
What HTTPS requests did the external destination receive?

### Evidence Needed
- Request timestamps
- Source address
- HTTP request path
- Submitted byte count
- Request order

### Observed Evidence
The external HTTPS server log records two POST requests from 192.168.56.121:

1. At approximately 14:16:32 Kali local time:
   - POST /api/report
   - 111 bytes submitted

2. At approximately 14:17:20 Kali local time:
   - POST /api/cache
   - 390 bytes submitted

The Kali server timestamps and Ubuntu audit/PCAP timestamps use different local/time-zone representations but correspond to the same lab activity sequence.

### Interpretation
The external server independently confirms two outbound data submissions from FIN-WS17.

The first request is consistent with the legitimate finance_sync.sh activity and the known 111-byte daily Finance summary.

The second request occurred immediately after the Finance-file archive was created and corresponds with the second HTTPS session. Its larger 390-byte body is consistent with transmission of the temporary compressed archive.

The request log confirms that data was submitted to the external server, but it does not by itself establish the contents of the second request.

### Confidence
High confidence that two POST requests reached the external server.

High confidence that the second POST correlates with the document_cache.sh execution sequence.

### Next Step
Examine the preserved received-data body carefully to determine whether the second POST actually contains the staged Finance archive.

## Investigation Step 5 — Received Data Validation

### Question
What did the external server actually receive during the second HTTPS POST?

### Evidence Needed
- Second request body
- File-type identification
- Archive contents
- Correlation with previously observed Finance files

### Observed Evidence
The preserved external-server received-data file was separated into its two known request bodies:

- First request body: 111 bytes
- Second request body: 390 bytes

File identification showed that the 390-byte second request body is gzip-compressed data.

Listing the archive contents without extraction showed:

- home/mreynolds/Documents/Finance/Q3_budget.csv
- home/mreynolds/Documents/Finance/vendor_payments.csv

These are the same two Finance files previously observed being read by tar during the document_cache.sh process sequence.

### Interpretation
The second HTTPS POST transmitted a compressed archive containing two Finance files to the external server.

This moves the finding beyond possible staging: the evidence now confirms outbound transfer of Finance files.

The activity is strongly consistent with data exfiltration behavior. However, whether document_cache.sh was authorized or expected remains unresolved, so a confirmed security compromise has not yet been declared.

### Confidence
High confidence that Q3_budget.csv and vendor_payments.csv were transmitted to the external server.

Medium-to-high confidence that the transfer was unauthorized pending validation of the script's business purpose.

### Next Step
Verify that the copies received by the external server are identical to the original Finance files, then determine whether document_cache.sh has any legitimate or authorized business purpose.

## Investigation Step 6 — Transmitted File Integrity Validation

### Question
Are the Finance files received by the external server identical to the original files on FIN-WS17?

### Evidence Needed
- SHA-256 hashes of the original Finance files
- SHA-256 hashes of the files recovered from the second HTTPS upload

### Observed Evidence

Q3_budget.csv:

Original FIN-WS17 SHA-256:
59e056b7075770c20cba2a4b265e764fb423f418153b8fd46a705850ae3545f9

External-server received copy SHA-256:
59e056b7075770c20cba2a4b265e764fb423f418153b8fd46a705850ae3545f9

vendor_payments.csv:

Original FIN-WS17 SHA-256:
6dfc38b02c7da0c1bc5165a3b391495e03a993f21c63457904883ac95e64eb07

External-server received copy SHA-256:
6dfc38b02c7da0c1bc5165a3b391495e03a993f21c63457904883ac95e64eb07

### Interpretation
The hashes match exactly. This confirms that the two Finance files recovered from the external HTTPS upload are byte-for-byte identical to the original Finance files on FIN-WS17.

The investigation therefore confirms that Finance data was packaged and successfully transmitted to the external destination.

Whether the transfer was authorized remains the principal unresolved question.

### Confidence
High

### Next Step
Determine whether document_cache.sh has an authorized or legitimate business purpose before declaring the activity malicious or the workstation compromised.

## Investigation Step 7 — document_cache.sh Metadata

### Question
What does the filesystem metadata reveal about document_cache.sh?

### Evidence Needed
- File path
- Ownership
- Permissions
- Size
- Creation and modification timestamps

### Observed Evidence
document_cache.sh is located at:

/home/mreynolds/.local/bin/document_cache.sh

Metadata shows:

- Owner: mreynolds
- Group: mreynolds
- Permissions: 0775
- Size: 338 bytes
- Birth time: 2026-09-06 17:41:20 UTC
- Modification time: 2026-09-06 17:41:20 UTC
- Change time: 2026-09-06 17:41:23 UTC

The script resides in the user's hidden .local/bin directory rather than a system-wide application directory.

### Interpretation
The file is executable and owned by the Finance user account. Its location and recent creation time warrant additional scrutiny, but filesystem metadata alone does not establish who authored the script, why it exists, or whether it was authorized.

### Confidence
High confidence regarding the filesystem metadata.

Low confidence regarding authorization or intent based on metadata alone.

### Next Step
Examine the contents of document_cache.sh to determine exactly what actions it performs and whether the code contains any indication of legitimate business purpose.

## Investigation Step 8 — document_cache.sh Content Review

### Question
What is document_cache.sh explicitly programmed to do?

### Evidence Needed
- Script commands
- Source files
- Temporary files
- Destination
- Cleanup behavior
- Any embedded indication of business purpose

### Observed Evidence
document_cache.sh performs the following actions:

1. Defines a temporary archive:
   /tmp/finance-cache-$USER.tar.gz

2. Uses tar with gzip compression to package:
   - /home/mreynolds/Documents/Finance/Q3_budget.csv
   - /home/mreynolds/Documents/Finance/vendor_payments.csv

3. Suppresses tar error output with:
   2>/dev/null

4. Uses curl to POST the archive to:
   https://finance-sync.local/api/cache

5. Stores the server response at:
   /tmp/cache-response.txt

6. Deletes the temporary Finance archive after the transfer with:
   rm -f "$CACHE"

The script contains no comments, authorization reference, business description, logging explanation, or other embedded documentation describing a legitimate purpose.

### Interpretation
The script's programmed behavior matches the independently observed evidence:

Finance files -> compressed archive -> HTTPS POST -> temporary archive deletion.

The behavior is consistent with data staging and exfiltration techniques. The absence of embedded business-purpose documentation increases concern but does not by itself establish malicious intent or compromise.

### Confidence
High confidence regarding what the script does.

Medium-to-high confidence that the activity is suspicious.

### Next Step
Compare document_cache.sh with the known Finance synchronization process to identify whether the two workflows have materially different purposes and behaviors before determining the initial disposition.

## Investigation Step 9 — Workflow Comparison

### Question
How does document_cache.sh differ from the known Finance synchronization workflow?

### Evidence Needed
- finance_sync.sh contents
- document_cache.sh contents
- Files collected
- Destination paths
- Temporary-file behavior
- Cleanup behavior

### Observed Evidence

finance_sync.sh:

- Reads one defined report:
  /home/mreynolds/Reports/daily_summary.txt
- Sends that report directly to:
  https://finance-sync.local/api/report
- Stores the response in:
  /home/mreynolds/Reports/sync-response.txt
- Does not create an archive.
- Does not collect Finance source documents.
- Does not delete staged data after transmission.

document_cache.sh:

- Collects two Finance source files.
- Creates a temporary compressed archive.
- Sends the archive to:
  https://finance-sync.local/api/cache
- Stores its response in /tmp.
- Deletes the temporary archive immediately afterward.

### Interpretation
The two workflows use the same HTTPS service but have materially different behavior.

finance_sync.sh has a narrow reporting function, while document_cache.sh collects multiple Finance documents, stages them in a temporary archive, transfers the archive, and removes the staged file afterward.

This distinction increases concern that document_cache.sh is not simply another instance of the normal reporting workflow.

### Confidence
High confidence regarding the behavioral differences.

### Next Step
Check the workstation baseline or approved-process record to determine whether finance_sync.sh and document_cache.sh are documented as authorized business processes.

## Investigation Step 10 — Baseline Authorization Review

### Question
Is document_cache.sh documented as an authorized Finance business process?

### Evidence Needed
- Workstation baseline
- Approved-process designation
- Identification of known Finance utilities

### Observed Evidence
The FIN-WS17 system profile identifies:

Authorized Business Process:
finance_sync.sh

Additional User Utility:
document_cache.sh

The baseline does not identify document_cache.sh as an authorized business process.

### Interpretation
finance_sync.sh is explicitly documented as the known authorized Finance workflow.

document_cache.sh exists on the workstation but is categorized only as an additional user utility. This means the available baseline does not establish an approved business purpose for document_cache.sh.

This increases concern when combined with the confirmed archive-and-transfer behavior, but absence from the authorized-process designation alone is not sufficient to prove malicious intent.

### Confidence
High confidence regarding the baseline designation.

Medium-to-high confidence that document_cache.sh requires escalation or further validation.

### Next Step
Determine whether document_cache.sh was configured to run automatically or persist on the workstation, or whether its execution appears to have been a one-time/manual event.

## Investigation Step 11 — User Cron Persistence Check

### Question
Was document_cache.sh configured to execute automatically through the mreynolds user crontab?

### Evidence Needed
- User crontab entries
- References to document_cache.sh
- Scheduled execution configuration

### Observed Evidence
The command:

sudo crontab -u mreynolds -l

returned:

no crontab for mreynolds

### Interpretation
There is no user-level cron configuration for mreynolds. Therefore, the available evidence does not support persistence or automated execution through the mreynolds crontab.

This does not exclude other scheduling or persistence mechanisms.

### Confidence
High

### Next Step
Check system-wide cron locations for any reference to document_cache.sh.

## Investigation Step 12 — System-Wide Cron Check

### Question
Was document_cache.sh configured to execute automatically through system-wide cron?

### Evidence Needed
- References to document_cache.sh under /etc/cron*
- Scheduled system cron entries

### Observed Evidence
A recursive search of the standard system-wide cron locations returned no references to document_cache.sh.

### Interpretation
There is no evidence that document_cache.sh was configured for persistence or automated execution through standard user or system-wide cron mechanisms.

This reduces support for the persistence hypothesis through cron but does not exclude other scheduling or startup mechanisms.

### Confidence
High

### Next Step
Check systemd services and timers for any reference to document_cache.sh.

## Investigation Step 13 — systemd Persistence Check

### Question
Was document_cache.sh configured to execute automatically through systemd services or timers?

### Evidence Needed
- References to document_cache.sh in systemd unit files
- Service or timer configuration

### Observed Evidence
A recursive search of:

- /etc/systemd/system
- /usr/lib/systemd/system

returned no references to document_cache.sh.

### Interpretation
There is no evidence that document_cache.sh was configured for persistence or automated execution through standard systemd services or timers.

Combined with the prior cron checks, the current evidence favors a one-time or manually initiated execution over a persistent scheduled mechanism.

### Confidence
High

### Next Step
Check the mreynolds shell history for evidence of manual execution or creation of document_cache.sh.

## Investigation Step 14 — Shell History Check

### Question
Is there shell-history evidence showing manual creation or execution of document_cache.sh by mreynolds?

### Evidence Needed
- Shell history files in /home/mreynolds
- References to document_cache.sh
- Commands creating or executing the script

### Observed Evidence
A search for visible history files in /home/mreynolds returned no results.

### Interpretation
There is no shell-history evidence available to establish that mreynolds manually created or executed document_cache.sh.

The absence of a history file does not prove that the activity was automated, unauthorized, or malicious. It simply means shell history cannot resolve the question.

### Confidence
High confidence that no visible history file was present.

Low confidence regarding how the script was initiated.

### Next Step
Review available audit records around the script creation time to determine whether the script's creation can be attributed to a process or user context.

## Investigation Step 15 — Script Creation Provenance

### Question
Can the preserved final audit evidence identify who or what created document_cache.sh?

### Evidence Needed
- Audit records covering the script creation time
- File creation events
- Process or user attribution

### Observed Evidence
document_cache.sh has a filesystem birth time of approximately 17:41:20 UTC.

A search of the preserved final audit log for the period 17:40:00 through 17:42:00 UTC returned:

<no matches>

### Interpretation
The preserved final audit evidence does not cover the script creation window.

Therefore, the investigation cannot determine from the final evidence set who created document_cache.sh or what process created it.

Earlier pretest/setup evidence will not be used for incident attribution because it belongs to lab construction rather than the final scenario evidence.

### Confidence
High confidence regarding this evidentiary limitation.

### Next Step
Assess the evidence collected so far and determine the appropriate initial disposition without overstating script provenance or user attribution.

## Investigation Step 16 — Initial Disposition

### Question
What disposition is supported by the evidence collected so far?

### Confirmed Findings
- FIN-WS17 established two outbound HTTPS sessions to the external destination.
- The first session was associated with the documented Finance synchronization workflow.
- The second session was associated with document_cache.sh.
- document_cache.sh collected Q3_budget.csv and vendor_payments.csv.
- The files were compressed into a temporary archive.
- The archive was transmitted to the external HTTPS server.
- The temporary archive was deleted after transmission.
- The external server received copies of both Finance files that were byte-for-byte identical to the originals.
- finance_sync.sh is documented as the authorized business process.
- document_cache.sh is not documented as an authorized business process.
- No cron or systemd persistence mechanism was identified for document_cache.sh.

### Unresolved Questions
- Who created document_cache.sh?
- Who or what initiated its execution?
- Was document_cache.sh approved through a process not represented in the available baseline?
- Is the external destination authorized for receiving Finance source documents?
- Is there additional activity outside the preserved evidence window?
- Has the workstation experienced any broader compromise?

### Disposition
Confirmed outbound transfer of Finance data through an additional user utility whose business authorization has not been established.

The activity should be treated as a likely security incident and escalated for containment and authorization validation.

The evidence does not yet support declaring that mreynolds personally performed the transfer or that FIN-WS17 is fully compromised.

### Risk Assessment
High

### Confidence
High confidence that Finance data was transferred externally.

Medium-to-high confidence that the transfer was unauthorized.

Low confidence regarding actor attribution and script provenance.

### Recommended Immediate Action
Preserve the workstation and collected evidence, escalate to the SOC Manager, validate the business authorization of document_cache.sh and the external destination, and prepare targeted network containment of FIN-WS17 if directed.

Avoid powering off the workstation because doing so could destroy volatile evidence.

---

## Step 17 — 11:40 Investigation Pivot

### Question

Does learning that mreynolds installed the software establish that the activity was legitimate?

### Evidence Needed

- Employee explanation.
- Software authorization status.
- Email and download provenance.
- File identity.
- Software behavior.
- Vendor/service authenticity.

### Observed Evidence

- mreynolds installed the utility earlier that morning.
- He stated that a known Finance vendor emailed him a link.
- He believed the utility was required to convert Finance data for that day's report.
- IT did not deploy the software.
- Security did not approve it.
- The application is unsigned.
- Endpoint security tooling did not classify it as malware.
- The original email and download site were not independently verified.

### Interpretation

Employee installation establishes how the software reached the workstation but does not establish that the software was legitimate.

Likewise, unsigned and unapproved status increase concern but do not establish malware.

### Confidence

High confidence regarding employee installation and lack of IT/Security approval.

Low confidence regarding vendor authenticity and ultimate root cause.

### Next Step

Validate the exact artifact and compare its actual behavior with its represented business purpose.

---

## Step 18 — Artifact and Behavior Validation

### Question

Does document_cache.sh behave like the data-conversion utility described to the employee?

### Evidence Needed

- SHA-256.
- Static script review.
- Filesystem output.
- External server behavior.

### Observed Evidence

The live and preserved copies of document_cache.sh produced the same SHA-256:

`1ee17971ce3cfb330457383ed019631b12ef9a8d738c560b1aad795329ee0c1c`

Static analysis showed that document_cache.sh:

1. Creates a compressed archive.
2. Adds Q3_budget.csv and vendor_payments.csv.
3. Sends the archive externally using HTTPS POST.
4. Deletes the temporary archive.

No observable data-conversion logic was present.

A search of the user's home directory during the relevant lab interval identified no apparent converted Finance output file.

### Interpretation

The observed client behavior does not match the stated conversion purpose.

This materially increases suspicion but does not prove malware.

### Confidence

High confidence that the investigated script does not perform an observable data-conversion function.

### Next Step

Determine whether conversion occurs on the external service and assess service identity.

---

## Step 19 — External Service Validation

### Question

Does the external service perform conversion or provide independently authenticated vendor identity?

### Evidence Needed

- Preserved server code.
- TLS certificate.
- Client TLS behavior.

### Observed Evidence

The external server:

- Accepts uploaded request bodies.
- Appends the data to received-data.bin.
- Returns `Upload received`.
- Performs no observable conversion.
- Returns no converted output.

The TLS certificate:

- Uses `CN=finance-sync.local`.
- Is self-signed.
- Was not independently tied to the known Finance vendor.

document_cache.sh uses `curl -k`, disabling normal TLS certificate validation.

### Interpretation

Neither the client nor server performs the represented conversion function.

The service identity also cannot be independently authenticated from the available TLS evidence.

This strengthens phishing, impersonation, vendor-compromise, or Trojanized-software hypotheses, while none is individually proven.

### Confidence

High confidence regarding observed client/server behavior.

Low confidence regarding the identity and intent of the software supplier.

### Next Step

Maintain containment and provide a safe business-continuity path while completing classification.

---

## Step 20 — Decision Point #3

### Question

Should FIN-WS17 be reconnected because Finance faces a two-hour reporting deadline?

### Observed Evidence

- Confirmed external Finance-data transfer.
- Recently introduced unapproved software.
- Represented conversion purpose contradicted by observed behavior.
- External endpoint not independently authenticated.
- Finance has an urgent legitimate business need.

### Decision

Keep FIN-WS17 isolated and powered on.

Move Finance work to a clean trusted workstation.

Recover only validated business files and use an approved conversion method.

### Interpretation

Business pressure affects how continuity is provided but does not justify restoring an unresolved high-risk endpoint to the network.

### Confidence

High confidence that continued containment is justified.

### Next Step

Complete final classification and remediation recommendations.

---

## Step 21 — Final Classification

### Question

What classification is supported by the totality of the evidence?

### Observed Evidence

The investigation confirmed that Finance data was transmitted externally through unapproved and unverified software whose observed behavior did not match its represented purpose.

The investigation did not prove that:

- document_cache.sh is malware.
- mreynolds acted maliciously.
- the vendor sent the email.
- the vendor was compromised.
- an external attacker controlled FIN-WS17.

### Final Classification

**Confirmed Security Incident — unauthorized external transmission of Finance data through unapproved and unverified software, with malware status and ultimate root cause unresolved.**

### Confidence

High confidence that a security-impacting unauthorized data transfer occurred.

Medium-high confidence that containment and remediation are required.

Low confidence regarding malware classification, supplier identity, and ultimate root cause.

### Final Next Step

Maintain containment, preserve evidence, validate the vendor independently, assess possible data exposure, remediate FIN-WS17, and restore Finance operations through trusted systems and approved software.
