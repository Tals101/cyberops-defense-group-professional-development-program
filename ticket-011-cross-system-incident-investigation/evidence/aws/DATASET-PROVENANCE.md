# AWS Dataset Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These records are generated for an authorized training
scenario. They are not exports from a real AWS account.

## Time Reference

The simulated incident date is November 2, 2026.

All eventTime fields are UTC.

The records contain routine activity before and during
the suspicious-activity window.

## Source Data

- cloudtrail-synthetic.jsonl
- reference-context-synthetic.json

## Design

Twelve synthetic API activity records include:

- Expected reporting automation
- Reporting credentials used from an unfamiliar IP
- Successful reporting-bucket access
- Denied sensitive-bucket access
- Denied elevated-role assumption
- Approved administrator activity from another IP
- Routine backup operations
- Simultaneous authorized reporting operations

## Analysis Limitations

The record set contains intentionally modeled outcomes.

It does not establish a real breach, prove data
exfiltration, or demonstrate a Kubernetes-to-AWS or
Linux-to-AWS connection.

CloudTrail-style GetObject success is an indication
of an allowed API request in this simulation. Actual
object content transfer would require additional
evidence.

The synthetic reference context is provided for
training evaluation. It is not independently verified
business authorization evidence.

Do not infer causation solely from event timestamps.

No real AWS API calls or account changes were made.