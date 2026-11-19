# Ticket 012 - Correlation Detector Design

## Objective
Identify suspicious application communication by
correlating multiple independent telemetry dimensions.

## Detection Dimensions

1. Workload identity
   - Application or pod identity
   - Claimed service identity
   - Identity inconsistencies

2. Network destination
   - Approved versus unapproved destination
   - Destination service and port
   - Unexpected communication

3. Deployment changes
   - Configuration modification timestamp
   - Previous and current destination
   - Temporal relationship to network activity

4. Authorization results
   - Successful requests
   - Rejected requests
   - Security control events

## Correlation Approach
Evaluate multiple dimensions together within a defined
time window instead of alerting on one field alone.

## Data Quality Requirements
- Normalize timestamps to UTC.
- Handle missing or malformed fields.
- Identify duplicate events.
- Account for clock skew.
- Avoid treating client-supplied identity as verified identity.

## Expected Outputs
- Machine-readable detection results
- Supporting event references
- Human-readable explanations
- Severity and confidence assessments

## Validation Requirements
- At least 15 automated tests
- At least 4 false-positive scenarios
- Comparison against a baseline detection rule
- Documented detection limitations

## Current Status
Design prepared.
Detector implementation not yet started.
