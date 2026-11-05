# Linux Dataset Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These 18 Linux events were deliberately authored
for a training scenario. They are not collected
SSH logs, auditd logs, cron logs, or network captures
from any real Linux system.

Generated UTC: 2026-11-03T18:54:14.4543213+00:00
Scenario date: 2026-11-02
Event timestamp timezone: UTC
Modeled host: linux-reporting-01

## Generated Files

- linux-auth-synthetic.jsonl: 9 events
- linux-process-persistence-synthetic.jsonl: 6 events
- linux-network-synthetic.jsonl: 3 events

Generator: generate-linux-synthetic-8b.ps1
Generator SHA256: AF61E698480B32EC7978D77D2BDBC028E5F08C6F2BB8808A9AAC27434C1F575E

## Existing Source Anchors

AWS timeline SHA256: 4900A2274D355AFF8D6D5174B375D5DB48B943F8A8046B17EDABE31FD78E574F
Kubernetes provenance SHA256: D117C0F425DD0DAD9EFE7D54058CDE00F0847E47A2D3470CC67DC0CAF2D5336E

These existing sources supplied investigation
context. The Linux events themselves were newly
created, not extracted from those source records.

## Synthetic Scenario

- Routine administrative SSH activity
- Two failed SSH attempts from 203.0.113.77
- A subsequent successful SSH session for ops-runner
- One denied sudo authorization
- A user-level cron modification
- A modeled cron process execution
- An outbound connection to 203.0.113.77
- Later administrative inspection
- Routine network and process events

The source-IP and destination-IP overlap with
other synthetic datasets is intentional.

It does not prove a common operator, credential
theft, exfiltration, or causal linkage.

The user-level cron event is not a real installed
scheduled task. No persistence mechanism was
installed on any host.

203.0.113.0/24, 198.51.100.0/24, and 192.0.2.0/24
are documentation-only network ranges.

## Interpretation Boundaries

A successful modeled SSH authentication is not
proof that access was unauthorized.

A modeled cron modification is not proof of
malicious persistence.

A modeled allowed TCP connection does not prove
data transfer or exfiltration.

Event timestamps alone cannot establish causation.

No AWS access-key use is attributed to the Linux
processes by these event records.

The 09:05 containment stop gate is not modeled
as an actual containment action.

## Reproduction

Run the saved PowerShell generator with its
ProjectRoot and GeneratorPath arguments in a
clean copy of the Ticket 011 project.

The generator intentionally refuses to overwrite
existing dataset files.

## Safety

No live Linux host was accessed.
No SSH connection was initiated.
No cron entry, systemd unit, or service was changed.
No Kubernetes, Helm, Docker, or AWS resources
were modified.