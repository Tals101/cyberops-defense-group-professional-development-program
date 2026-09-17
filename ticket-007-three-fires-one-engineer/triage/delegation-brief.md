# Ticket #007 — Delegation Brief

## Objective

Determine whether HR-LT-51 shows evidence of the same or related malicious activity observed on HR-LT-44.

## Scope

HR-LT-51 only, plus evidence directly related to its communication with the shared external destination.

## Evidence to Collect

- EDR process tree around the connection time
- Processes responsible for the network connection
- Email or document activity preceding the connection
- Persistence indicators
- Credential-access indicators
- Relevant authentication activity
- Additional connections to the same destination
- File hashes or suspicious artifacts if identified

## Actions Authorized

- Collect and preserve endpoint telemetry
- Review EDR and Windows logs
- Validate the process responsible for the connection
- Preserve suspicious files without executing them
- Perform read-only IOC searches
- Report findings and confidence

## Actions Requiring My Approval

- Network isolation of HR-LT-51 unless active malicious activity is clearly occurring
- Account disabling
- File deletion
- Remediation or reimaging
- Blocking infrastructure that could affect other systems

## When to Report Back

Report initial findings after rapid triage and immediately if evidence supports active compromise.

## Escalation Conditions

Escalate immediately if you identify:
- Suspicious execution linked to the destination
- Credential theft
- Persistence
- Lateral movement
- Sensitive-data access
- Repeated or continuing suspicious network activity
- Evidence that additional systems are involved
