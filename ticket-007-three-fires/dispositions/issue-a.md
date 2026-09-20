# Issue A — Privileged SSH Access

**Disposition: Likely Benign / Operational Process Failure**

## Basis for the decision

The source was traced to a newly provisioned administrator workstation, and the `sysadmin` account owner confirmed the session. The privileged commands available for review matched routine maintenance; none of the observed commands was malicious. The maintenance activity had not been entered on the SOC calendar, which explains why an otherwise authorized login required extra validation.

**Confidence:** High for the likely-benign conclusion based on the source, owner confirmation, and reviewed activity.

## Impact and follow-through

I found no confirmed compromise or direct business disruption from this access. The meaningful issue is lost SOC visibility into legitimate production work: an undocumented change can consume analyst time and complicate the response to a genuine alert.

I checked the source and privileged activity and preserved the relevant records. Infrastructure Operations should own the missed maintenance notification and verify that future administrative work reaches the SOC through the expected change process.

**Closure condition:** The observed session continues to fit authorized maintenance, and responsibility for fixing the notification gap is assigned.
