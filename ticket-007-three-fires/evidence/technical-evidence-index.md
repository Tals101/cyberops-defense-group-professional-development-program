# Ticket #007 — Evidence Index

This index explains why each artifact is in the package. The source files themselves have been retained as collected; descriptions here are not substitutes for the logs or event records.

## Issue A — Privileged access

| File | What I used it for |
|---|---|
| `01-issue-a-ssh-login.txt` | Identify the `sysadmin` authentication event and recorded source. |
| `04-issue-a-asset-inventory.txt` | Check the administrative host's documented role and access. |
| `06-issue-a-privileged-commands.txt` | Review the commands visible during the active session. |
| `08-issue-a-active-session.txt` | Confirm that the session was still connected when I revisited A. |

## Issue B — Initial endpoint assessment

| File | What I used it for |
|---|---|
| `01-encoded-powershell-event.txt` | Record PowerShell execution in Windows Security Event ID 4688. |
| `02-word-encoded-powershell-event.txt` | Establish Word as the parent of the encoded PowerShell process. |
| `03-simulated-edr-alert.txt` | Preserve the labeled High Severity scenario alert and reported block. |
| `04-decoded-powershell-command.txt` | Check the decoded command rather than judging it by encoding alone. |
| `hr-lt-44-marker.txt` | Confirm the benign marker produced by the controlled command. |

## Issue B — Deeper checks

| File | What I used it for |
|---|---|
| `deep-investigation/01-hr-lt-44-external-connection.log` | Verify successful contact with the controlled server. |
| `deep-investigation/02-persistence-check.txt` | Document the scheduled-task and Run-key checks performed. |
| `deep-investigation/03-credential-access-check.txt` | Record the query and its visibility limitations; a negative match is not proof of absence. |
| `deep-investigation/04-simulated-email-evidence.txt` | Represent the scenario's sender, attachment, and arrival timing. |
| `deep-investigation/05-endpoint-user-context.txt` | Explain how CyberHub stands in for HR-LT-44 in the lab. |
| `deep-investigation/06-data-access-event.txt` | Show that a separate controlled PowerShell process could read sample HR data. |
| `deep-investigation/07-lateral-movement-check.txt` | Record the limited review for common lateral-movement indicators. |
| `deep-investigation/08-two-host-same-destination.log` | Show two lab systems contacting the same endpoint; not a shared-root-cause finding. |
| `deep-investigation/09-hr-lt-51-delegated-findings.txt` | Capture the separate HR-LT-51 assessment and limits of that correlation. |

## Issue C — Portal availability and request timing

| File | What I used it for |
|---|---|
| `02-issue-c-portal-access.log` | Review HTTP 200/500 responses alongside unusual paths. |
| `03-issue-c-config-change-record.txt` | Establish the scenario's deployment and rollback context. |
| `05-issue-c-error-vs-unusual-requests.txt` | Compare when errors began with the suspicious requests observed. |
| `07-issue-c-current-error-sample.txt` | Preserve the 20-request pre-rollback response sample. |

## Reading the evidence correctly

Windows and Linux events came from the controlled lab. Enterprise EDR, mail, asset, and change-management details are labeled scenario records where such services were unavailable. The controlled network tests used harmless content. I have not treated a negative search as conclusive absence or a demonstration of file access as proof that the suspicious process took data.
