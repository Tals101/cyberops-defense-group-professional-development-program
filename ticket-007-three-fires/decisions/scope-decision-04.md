# Ticket #007 — Scope Decision #4

*Decision at the 10:50 second-workstation alert, before delegated triage returned.*

## Why HR-LT-51 enters the investigation

HR-LT-51 contacted the destination already under review for HR-LT-44. That is enough to ask whether another HR endpoint is involved, but it is not enough to conclude that both users experienced the same attack.

**Scope for now:** Keep HR-LT-44 as the primary incident workstation, add HR-LT-51 for focused triage, and search relevant environment telemetry for the destination and related indicators. The possible investigation scope has widened; the number of **confirmed compromised** hosts has not automatically doubled.

## Containment call

Maintain the HR-LT-44 containment decision. Do not isolate HR-LT-51 just for a destination match when it has no reported High Severity EDR alert or matching execution chain. Move to containment promptly if its review shows suspicious execution, persistence, credential access, repeated malicious communication, or other credible compromise evidence.

## Help requested

I will ask for one additional engineer with a bounded HR-LT-51 assignment and retain the HR-LT-44 investigation and overall incident decisions. Notify the SOC Manager, SOC analyst, and HR IT/support; bring in Network Engineering for destination-wide searching or any proposed block.

## Assumption to avoid

A common IP or hostname can serve unrelated applications, shared infrastructure, or a compromised legitimate service. If I assume a common root cause before checking the processes and user activity, I risk isolating an innocent workstation and overlooking the actual mechanism on either host. Correlation is the reason to investigate, not the conclusion.
