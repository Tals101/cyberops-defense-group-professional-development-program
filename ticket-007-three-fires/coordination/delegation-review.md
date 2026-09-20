# Ticket #007 — Delegation Review

## Source and authorization check — Issue A

I gave the SOC analyst a specific question: identify the unfamiliar source, check whether the `sysadmin` login was expected, and look for associated alerts. Read-only asset and SOC access was enough to answer it. That work ran while I investigated B, so it did not duplicate my endpoint review. The source was linked to an admin workstation, and later confirmation established that the activity was maintenance.

The timing was appropriate: I delegated at initial triage and returned to A when the active session and privileged commands were reported. In retrospect, Infrastructure Operations could have been asked for the administrator's maintenance confirmation earlier; doing so may have shortened the period of uncertainty.

## Portal validation and restoration — Issue C

Operations was already responding when the portal alert arrived. I asked them to preserve the logs, line up the change with the errors, keep a rollback ready, and report service behavior afterward. They had the authority to restore their own service. Security retained responsibility for the unusual-request question rather than repeating Operations' health checks.

The rollback result was useful: errors moved back toward baseline. I followed up by leaving traffic review open. A formal post-rollback health summary would have made the handoff even clearer, and I would request one earlier next time.

## Second workstation — HR-LT-51

When the second destination match appeared, I requested an additional engineer to test whether HR-LT-51 had the same or related execution. The brief limited the work to that host and relevant connection evidence. Read-only collection was authorized, while isolation and other disruptive steps remained approval-dependent.

The engineer found the shared destination but not the Word-to-PowerShell chain, EDR High alert, persistence indicators, credential-access indicators, or suspicious authentication. That was decision-changing information: I could keep HR-LT-44 as the primary incident system without isolating HR-LT-51 on correlation alone. It also saved me a context switch while I managed the main response.

## What I would adjust

I kept the cross-workstream decisions, containment approval, and incident scope with me. Those required integrating evidence from several owners. I could have delegated the environment-wide destination search to Network Engineering sooner, alongside the HR-LT-51 review. The strongest handoffs in this exercise had a narrow question, clear authority, a useful return product, and explicit reasons to escalate.
