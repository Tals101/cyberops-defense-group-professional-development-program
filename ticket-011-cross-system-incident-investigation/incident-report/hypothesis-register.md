# Ticket #011 - Initial Incident Hypothesis Register

All hypotheses below are UNTESTED.

## H01 - Related Cross-System Compromise

A shared identity or access path could explain
AWS, Kubernetes, and Linux activity.

Status: UNTESTED

Required evidence:
Credential identity, network path, source attribution,
and independent cross-system corroboration.

## H02 - AWS Incident Only

AWS credential use may be unauthorized while
Kubernetes and Linux events are independent.

Status: UNTESTED

Required evidence:
AWS identity, authorization, role-assumption outcome,
and legitimate-use comparison.

## H03 - Kubernetes Incident Only

Runtime activity may represent an isolated
workload compromise unrelated to AWS or Linux.

Status: UNTESTED

Required evidence:
Process ancestry, Pod identity, credential access,
network destination, and audit events.

## H04 - Linux Incident Only

SSH activity and scheduled-task creation may
indicate unauthorized host access and persistence.

Status: UNTESTED

Required evidence:
Authentication identities, source attribution,
scheduled-task content, and process history.

## H05 - Benign or Partially Coincidental Activity

Some or all alerts may reflect legitimate operations
or independent events occurring close together.

Status: UNTESTED

Required evidence:
Approved automation schedules, administrator activity,
source-IP ownership, and business context.

## Decision Rule

Timestamp proximity alone does not establish causation.

Each hypothesis must be supported, contradicted, or
left inconclusive using preserved evidence.

Initial incident disposition: UNDETERMINED.
