# Ticket #007 — Three Fires, One Engineer

## Project overview

Three alerts reached the queue within minutes of one another. I had one set of hands, incomplete information, and several teams waiting for direction. The exercise was less about running every possible command than deciding where my attention would make the most difference, documenting why I changed course, and leaving the next person a usable record.

The three workstreams were:

- **Issue A:** An unfamiliar source established a privileged SSH session on APP-PROD-02.
- **Issue B:** Microsoft Word launched encoded PowerShell on HR-LT-44, triggering a High Severity EDR alert.
- **Issue C:** A customer portal began returning errors while unusual HTTP requests were appearing in its logs.

I worked through the alerts using Linux and Windows telemetry, controlled lab network traffic, and clearly identified scenario records for enterprise systems not present in my home lab.

## How the decisions unfolded

| Scenario time | Order of attention | Reason for the decision |
|---|---|---|
| 09:00 | B → A → C | The endpoint was still connected after Word launched encoded PowerShell. |
| 09:25 | C → A → B | Operations needed a rollback decision while customers were seeing portal errors. |
| 09:40 | B → C → A | The email origin and incomplete EDR prevention changed the endpoint risk. |
| 10:05 | B → C → A | The HR workstation had successfully contacted an external destination. |
| 10:50 | B → C → A | A second HR workstation warranted a broader search, not an automatic second compromise finding. |

The decision files preserve what was known **at the time of each choice**. Later information appears in later records rather than being folded into the earlier assessments.

## Where the investigations landed

**Issue A — Likely Benign / Operational Process Failure.** The account owner confirmed the SSH activity, the source was an authorized administrator workstation, and the observed commands fit routine maintenance. The outstanding action is to address why the SOC had no maintenance notice.

**Issue B — Confirmed Security Incident in the exercise scenario.** An email attachment preceded the Word-to-PowerShell process chain. PowerShell ran before EDR blocked a child process, and HR-LT-44 subsequently reached an external destination without an established business purpose. The controlled command used to reproduce this behavior was benign; it is not evidence of a real malicious payload. Persistence, credential theft, lateral movement, and HR data exfiltration were not confirmed.

**Issue C — Operational Issue with Security Follow-Up.** Error rates improved following rollback of a recent configuration change. Unusual requests remained worth reviewing, but their timing did not establish that they caused the outage or that exploitation succeeded.

HR-LT-51 contacted the same destination as HR-LT-44. A separate review found no matching Word-to-PowerShell activity or other supporting compromise indicators. I kept the broader indicator search open without treating the second workstation as compromised solely because of a shared destination.

## Where to start

- `Final_Incident_Report.pdf` — consolidated findings, limitations, response, and dispositions.
- `engineering-notebook.md` — the investigative questions, observations, and decisions in sequence.
- `triage/` — initial assessment, rapid findings, priority history, and attention log.
- `decisions/` — the original priority calls, interruptions, reassessments, and scope change.
- `communications/` — manager, Operations, and executive updates.
- `coordination/` — delegated work, stakeholder involvement, and incident actions.
- `dispositions/` — one final outcome for each of the three issues.
- `evidence/` — source artifacts, controlled test results, and a file-by-file index.

## Evidence boundaries

This repository is a **training investigation**. Windows process and Linux authentication events were generated in the lab; enterprise mail, asset inventory, and EDR records were represented by labeled scenario artifacts. The controlled external server returned a harmless test response. I have kept those distinctions visible because a demonstrated capability is not the same thing as proof that a threat actor used it.

## What I would carry into a real incident

The question is not simply which alert sounds worst. I need to weigh the impact of waiting against the cost of acting, find the next piece of evidence that could change a decision, and hand off bounded work without losing ownership of the incident as a whole.
