# Ticket #007 — Technical Evidence Package Index

## Issue A — Privileged Authentication

### 01-issue-a-ssh-login.txt
SSH authentication evidence showing the sysadmin login and source address.

### 04-issue-a-asset-inventory.txt
Asset information used to identify the source as an authorized administrative system.

### 06-issue-a-privileged-commands.txt
Sudo evidence showing the privileged commands executed during the active sysadmin session.

### 08-issue-a-active-session.txt
Evidence confirming the sysadmin session remained active during investigation.

---

## Issue B — Suspicious Endpoint Activity

### 01-encoded-powershell-event.txt
Windows Security Event ID 4688 evidence showing encoded PowerShell execution.

### 02-word-encoded-powershell-event.txt
Windows process-creation evidence confirming WINWORD.EXE launched encoded PowerShell.

### 03-simulated-edr-alert.txt
Clearly labeled simulated High Severity EDR alert representing the Ticket #007 scenario.

### 04-decoded-powershell-command.txt
Safely decoded PowerShell command used during rapid triage.

### hr-lt-44-marker.txt
Benign marker created by the decoded PowerShell command.

---

# Issue B — Deep Investigation

### 01-hr-lt-44-external-connection.log
Controlled external-server evidence confirming successful outbound communication.

### 02-persistence-check.txt
Scheduled-task and Run-key persistence review.

### 03-credential-access-check.txt
Credential-access indicator review and logging limitations.

### 04-simulated-email-evidence.txt
Clearly labeled simulated email evidence representing the triggering attachment and suspicious sender context.

### 05-endpoint-user-context.txt
Mapping of the CyberHub lab host to scenario asset HR-LT-44 and HR user context.

### 06-data-access-event.txt
Controlled evidence showing PowerShell access to representative HR data.

### 07-lateral-movement-check.txt
Review for common lateral-movement indicators.

### 08-two-host-same-destination.log
External-server log showing two systems communicating with the same destination.

### 09-hr-lt-51-delegated-findings.txt
Delegated engineer findings showing that HR-LT-51 did not demonstrate the same suspicious execution chain.

---

## Issue C — Internet-Facing Portal

### 02-issue-c-portal-access.log
Portal access log showing normal responses, intermittent HTTP 500 errors, and unusual web requests.

### 03-issue-c-config-change-record.txt
Simulated Operations record documenting the recent portal configuration change.

### 05-issue-c-error-vs-unusual-requests.txt
Timing comparison between service errors and unusual requests.

### 07-issue-c-current-error-sample.txt
Twenty-request sample showing intermittent HTTP 500 responses before rollback.

---

## Evidence Handling Notes

The Ticket #007 lab combines real operating-system telemetry with clearly labeled simulated scenario records.

Simulated records are used only where the exercise references enterprise systems not available in the home lab, such as enterprise EDR, corporate email telemetry, and asset-management records.

Conclusions distinguish between observed lab evidence, simulated scenario evidence, and investigation limitations.
