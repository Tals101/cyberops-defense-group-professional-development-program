# Kubernetes Evidence Provenance - Ticket 011

## Classification

SYNTHETIC LABORATORY EVIDENCE

These are modeled Kubernetes audit, Falco-style
runtime, and network-flow records.

They are not exports from a production cluster
or observations collected from a running Pod.

## Scenario

A reporting-api Pod in the simulated
production-reporting namespace exhibits:

- Routine application and network activity
- A successful Kubernetes exec API operation
- An unexpected shell process
- A read of the Kubernetes ServiceAccount token file
- A connection to an unfamiliar external destination
- A denied Kubernetes Secret request
- A denied ephemeral-container modification
- A denied Deployment modification
- Later administrative workload inspection

## Relationship to AWS Evidence

The external address 203.0.113.77 appears as a
Kubernetes outbound destination in this dataset.

The same address appears as an AWS API source
in the separately generated AWS dataset.

This is a possible investigative association.
It is NOT proof of shared origin, credential theft,
a common operator, or causal linkage.

NAT mapping, destination attribution, process-to-
network attribution, AWS credential access evidence,
and independent infrastructure records are absent.

The modeled ServiceAccount token is a Kubernetes
identity credential, not an AWS access key.

## Evidence Limitations

All timestamps are UTC on November 2, 2026.

The synthetic workload context is a modeled snapshot,
not an authoritative live RBAC inspection.

A successful exec API operation does not prove who
spawned every subsequent process.

A token-file read does not prove successful token
exfiltration or AWS credential exposure.

An allowed network connection does not establish
its content, intent, or successful data transfer.

Denied workload modifications do not rule out
persistence mechanisms outside the modeled events.

No real cluster resources were created, changed,
deleted, or queried to generate these records.