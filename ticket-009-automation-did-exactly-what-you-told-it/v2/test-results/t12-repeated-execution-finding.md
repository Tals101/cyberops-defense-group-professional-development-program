# Ticket #009 — T12 Repeated Execution Finding

## Test

T12 — Repeated Execution Is Safe

## Expected Result

Repeated execution should:

- avoid duplicating completed changes;
- avoid unexpected additional automatic changes;
- preserve the intended blast-radius boundary across repeated executions.

## Observed Result

The second execution produced:

- nora.hayes — NO_ACTION — ALREADY_DISABLED
- kevin.brooks — NO_ACTION — ALREADY_DISABLED
- contractor.mills — DISABLE — SUCCESS

Changes made during second run:

1

## Finding

V2 is idempotent for identities already remediated.

It did not attempt to disable nora.hayes or kevin.brooks again.

However, the configured maximum of two state changes applies only to an individual execution.

The counter resets when another run begins.

As a result, contractor.mills, which had previously been staged because the first run reached its limit, became eligible for automatic remediation during the next run.

## Engineering Risk

A per-run action limit does not necessarily bound the blast radius of a remediation campaign.

Repeated scheduled executions could gradually remediate every eligible identity even when an earlier run stopped because the safety threshold was reached.

This could undermine the purpose of the run-level safety control.

## Root Cause

V2 does not persist the state of identities deferred because the remediation limit was reached.

The next execution therefore treats a deferred identity as a fresh AUTO_REMEDIATE candidate.

## Required Correction

An identity deferred because the safety limit was reached must not automatically become eligible again merely because another run starts.

V2 should persist deferred-action state.

A deferred identity should require an explicit review or release before automatic enforcement can occur in a later run.

This creates a campaign-level boundary in addition to the per-run boundary.

## Test Result

**FAIL — DESIGN GAP IDENTIFIED**

The failure will be preserved before corrective implementation.

T12 must be rerun after the cross-run control is implemented.
