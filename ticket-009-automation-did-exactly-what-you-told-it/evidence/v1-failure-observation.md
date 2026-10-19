# Ticket #009 — V1 Failure Observation

## Execution Result

V1 executed successfully against the preserved synthetic identity dataset.

The automation did not crash or generate an execution error.

It applied its configured rule as designed.

## Observed Remediation Results

V1 disabled five accounts:

1. nora.hayes
2. svc_finance_batch
3. svc_records_archive
4. contractor.mills
5. analytics.temp

V1 left five accounts enabled:

1. emma.reed
2. samir.patel
3. kevin.brooks
4. admin.ops
5. ingest.bridge

The observed result matched the pre-execution prediction.

## Finance Service Failure

After V1 execution, the simulated Finance application health check examined the identity dependency for:

Finance LedgerBridge

The required identity was:

svc_finance_batch

Observed identity state:

enabled=False

The health check recorded:

AUTHENTICATION_FAILURE dependency_account=svc_finance_batch reason=identity_disabled

The simulated application then reported:

APPLICATION_STATUS=FAILED

## Known Facts

- V1 disabled svc_finance_batch.
- svc_finance_batch is configured as a dependency of Finance LedgerBridge in the simulation.
- The Finance health check found the required identity disabled.
- The health check produced an authentication failure.
- The simulated application status was FAILED.

## Inference

The evidence supports the conclusion that disabling svc_finance_batch caused the simulated Finance application failure.

This relationship is stronger than simple timing correlation because the health check directly evaluated the configured service dependency and recorded the disabled identity as the authentication failure condition.

## Important Engineering Finding

V1 did not fail because its Python implementation malfunctioned.

V1 correctly executed an unsafe decision model.

The rule considered interactive-login age but ignored relevant context including:

- recent non-interactive activity;
- identity type;
- service dependencies;
- business purpose;
- ownership;
- approval state;
- lifecycle state.

The remediation decision was then converted directly into a state change without an approval boundary or impact check.

## Additional Blast-Radius Evidence

The Finance identity was not the only questionable remediation.

V1 also disabled:

- svc_records_archive, a legitimate approved service account;
- analytics.temp, an ambiguous identity with recent non-interactive activity and conflicting evidence.

At the same time, V1 left kevin.brooks enabled even though the account belongs to a terminated employee and is marked pending disable.

This demonstrates both:

- unsafe positive decisions; and
- unsafe negative decisions.

## Preservation Decision

V1 will not be modified at this stage.

The affected Finance account will not yet be added to an exception list.

The failed V1 code, input data, output state, remediation decisions, logs, and application-failure evidence will be preserved as incident evidence before redesign begins.
