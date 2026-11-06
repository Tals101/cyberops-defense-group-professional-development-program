# Ticket 011 - Linux Authentication and Persistence Investigation

Ticket: CYBEROPS-PDP-011
Analysis UTC: 2026-11-05T00:45:06.6613572+00:00

**Evidence classification: SYNTHETIC LABORATORY DATA**

## Executive Assessment

The 18 modeled Linux records present a sequence of
failed SSH authentication, successful SSH authentication,
user-level crontab modification, cron execution,
and an allowed outbound connection.

These are deliberately generated training events.
No actual Linux host compromise is established.

## Evidence Reviewed

- linux-auth-synthetic.jsonl: 9 records
- linux-process-persistence-synthetic.jsonl: 6 records
- linux-network-synthetic.jsonl: 3 records

Authentication SHA256: 71B513E1ED147187C8396591C1782E8A4215F14D4C6753B82FDB6EA7D89F3AAD
Process/persistence SHA256: CBBE9708903F19FF8BA8CC495BDBC0A15441CFD8CB92D58C899F6A7F9E40A1A3
Network SHA256: 5FFDA3A5C614C0E53C10B5BA33EBAF875BF4FC58F9685775184CDE67E14044C5

## Linux Event Timeline

All times are UTC on November 2, 2026.

| Time UTC | Event ID | Actor | Action | Outcome |
|---|---|---|---|---|
| 12:50:00 | lin-0001 | ops-admin | ssh.accepted | SUCCESS |
| 12:50:01 | lin-0002 | ops-admin | ssh.session_open | SUCCESS |
| 12:50:12 | lin-0010 | ops-admin | process.started | SUCCESS |
| 12:50:21 | lin-0016 | ops-admin | tcp.connect | ALLOWED |
| 13:03:10 | lin-0003 | ops-runner | ssh.failed_password | DENIED |
| 13:03:17 | lin-0004 | ops-runner | ssh.failed_password | DENIED |
| 13:04:02 | lin-0005 | ops-runner | ssh.accepted | SUCCESS |
| 13:04:03 | lin-0006 | ops-runner | ssh.session_open | SUCCESS |
| 13:05:59 | lin-0011 | ops-runner | user_crontab.modified | SUCCESS |
| 13:06:00 | lin-0012 | ops-runner | file.metadata_changed | SUCCESS |
| 13:06:25 | lin-0007 | ops-runner | sudo.authorization | DENIED |
| 13:07:00 | lin-0013 | ops-runner | cron.job_started | SUCCESS |
| 13:07:01 | lin-0017 | ops-runner | tcp.connect | ALLOWED |
| 13:07:02 | lin-0014 | ops-runner | process.exited | SUCCESS |
| 13:09:15 | lin-0008 | analyst-admin | ssh.accepted | SUCCESS |
| 13:09:20 | lin-0018 | analyst-admin | tcp.connect | ALLOWED |
| 13:10:30 | lin-0015 | analyst-admin | systemd_timer.inspected | SUCCESS |
| 13:12:00 | lin-0009 | ops-runner | ssh.session_close | SUCCESS |

## Finding F-LNX-01: SSH Authentication Sequence

Events: lin-0003, lin-0004, lin-0005, lin-0006.

The modeled ops-runner account has two failed SSH
password attempts from 203.0.113.77, followed by
a successful authentication and session opening.

The event sequence is suspicious within the
training scenario. It does not independently
prove that the successful login was unauthorized.

## Finding F-LNX-02: Possible User-Level Persistence

Events: lin-0011, lin-0012.

A user crontab modification is modeled under
ops-runner with the same session identifier as
the preceding SSH session.

The event refers to telemetry_diag.py.

This supports a modeled persistence hypothesis,
but approval, task content, and intent are unverified.

## Finding F-LNX-03: Process and Network Activity

Events: lin-0013, lin-0014, lin-0017.

The modeled cron job starts at 13:07:00 UTC.

A connection to 203.0.113.77:443 is recorded
at 13:07:01 UTC.

Both records carry process ID 1413 and
session ID cron-ops-runner-01.

This is an explicit relationship in the
synthetic records, not independently collected
process or packet-capture evidence.

An allowed connection does not establish
transferred content or exfiltration.

## Finding F-LNX-04: Privilege Escalation Denied

Event: lin-0007.

A modeled sudo authorization request targeting
root was denied. No successful privilege
elevation is established by this event.

## Finding F-LNX-05: Benign Alternatives

The dataset includes routine maintenance
and administrative review events.

A legitimate maintenance script, approved
scheduled task, or network-routing change
could explain some suspicious-looking activity.

No independent authorization records
have been provided to resolve those alternatives.

## Cross-System Assessment

The synthetic AWS timeline includes five
reporting-identity requests from 203.0.113.77.

The synthetic Kubernetes dataset also references
203.0.113.77 as an outbound destination.

The Linux dataset deliberately uses this
address for SSH activity and one outbound
connection.

These shared attributes are suitable for
correlation-engine testing.

They do not establish that the same machine,
operator, credential, or process caused
events in all three systems.

The Kubernetes ServiceAccount credential
must not be equated with the modeled AWS key.

## Hypothesis Status

H01 - Related cross-system compromise:
POSSIBLE BUT UNPROVEN.

H02 - AWS-only incident:
NOT EXCLUDED.

H03 - Kubernetes-only incident:
NOT EXCLUDED.

H04 - Linux-only incident:
SUPPORTED AS A SYNTHETIC SCENARIO;
ACTUAL UNAUTHORIZED ACCESS UNCONFIRMED.

H05 - Benign or independent events:
NOT EXCLUDED.

## Further Evidence Required

- Actual SSH and session authentication records
- Change approval and cron configuration history
- Process ancestry and executable integrity
- Real network flow, DNS, and transfer telemetry
- AWS credential custody and source attribution
- Kubernetes workload identity and network mapping
- Verified system clock and event collection coverage

## Disposition

Linux synthetic scenario: ANALYZED.
Real-world Linux compromise: NOT ESTABLISHED.
Malicious persistence: NOT ESTABLISHED.
Data exfiltration: NOT ESTABLISHED.
Cross-system causation: NOT ESTABLISHED.

This report does not authorize destructive
containment or any production changes.

No live Linux host, Kubernetes workload,
Helm release, or AWS environment was modified.