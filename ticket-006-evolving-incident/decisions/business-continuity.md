# Ticket #006 — Business Continuity Recommendation

## Objective

Allow Finance to complete legitimate reporting work without reconnecting or relying on FIN-WS17 while its security status remains unresolved.

## Immediate Recommendation

FIN-WS17 should remain network isolated and powered on for investigation.

Finance should continue work from a clean, trusted corporate workstation.

The reporting deadline should be supported through an alternate workflow rather than by restoring the affected workstation to normal use.

## Safe Continuity Plan

### 1. Provide a Clean Workstation

Assign Mark a known-good corporate workstation or approved virtual desktop.

Do not clone or restore the full FIN-WS17 environment onto the replacement system.

### 2. Recover Only Required Business Data

Use existing trusted sources first, such as:

- Approved Finance file shares.
- Corporate document repositories.
- Backups.
- Previously validated copies.
- Other trusted Finance systems.

If required files exist only on FIN-WS17, recover only the specific business documents needed for the report through a controlled Security/IT process.

### 3. Validate Recovered Files

Before placing recovered files on the clean workstation:

- Scan them with available security tooling.
- Confirm expected file type and contents.
- Record source and destination.
- Preserve hashes where appropriate.
- Avoid transferring scripts, executables, temporary archives, or unknown utilities.

### 4. Use an Approved Conversion Method

Finance should not use document_cache.sh or the unverified vendor download.

Use one of the following:

- An already-approved corporate conversion application.
- A known-good tool obtained and validated by IT.
- A trusted manual conversion workflow.
- A vendor-supplied utility only after independent validation.

### 5. Validate the Vendor Independently

Finance or Security should contact the known vendor using previously established contact information.

Do not validate the software by:

- Replying to the questionable email.
- Calling a phone number contained only in that email.
- Using contact information from the unverified download site.

Ask the vendor to confirm:

- Whether the email was sent by them.
- Whether the download URL belongs to them.
- Whether the software is theirs.
- The expected file hash and digital-signature status.
- The expected network behavior.
- Whether external upload of Finance files is part of the intended workflow.

### 6. Preserve FIN-WS17

Do not wipe, rebuild, or power off FIN-WS17 until required evidence has been collected and Security approves remediation.

Do not execute the questioned utility again for testing on the affected endpoint.

## Business Impact

The alternate workflow may introduce delay and require assistance from IT and Security.

However, it allows Finance to continue working toward the reporting deadline without exposing the network to the unresolved risk associated with FIN-WS17.

## Security Benefit

This approach:

- Prevents additional questionable outbound transfer from FIN-WS17.
- Preserves evidence.
- Limits movement of potentially unsafe software.
- Maintains Finance operations on a trusted system.
- Separates business continuity from incident containment.

## Escalation

If Finance cannot meet the reporting deadline using the alternate workflow, the delay should be escalated to Finance leadership and incident leadership as a business-risk decision.

The workstation should not be reconnected solely because the reporting deadline is approaching.

## Final Recommendation

Maintain containment of FIN-WS17.

Restore Finance productivity through a clean workstation, validated business data, an approved conversion process, and independent vendor verification.
