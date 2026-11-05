# Ticket 011 - Cross-System Source Schema Audit

Ticket: CYBEROPS-PDP-011
Generated UTC: 2026-11-05T00:47:53.6837970+00:00

Classification: SYNTHETIC SOURCE SCHEMA AUDIT

## Scope

Review seven existing synthetic JSONL event sources
without altering their original content.

Total source files: 7
Total source records: 42
AWS records: 12
Linux records: 18

## Source Schemas

### AWS_CLOUDTRAIL

Source: evidence\aws\cloudtrail-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 12

SHA256: 7F2CA74754DB29D78DBEE777F712BB74659D0A3FF895B77FF7114AF0A2CFAF78

Top-level fields:

awsRegion, datasetType, errorCode, eventID, eventName, eventSource, eventTime, eventVersion, outcome, recipientAccountId, requestID, requestParameters, resources, responseElements, sourceIPAddress, sourceSystem, userIdentity

All discovered schema paths:

awsRegion, datasetType, errorCode, eventID, eventName, eventSource, eventTime, eventVersion, outcome, recipientAccountId, requestID, requestParameters, requestParameters.targetResource, resources, resources.ARN, responseElements, sourceIPAddress, sourceSystem, userIdentity, userIdentity.accessKeyId, userIdentity.arn, userIdentity.principalId, userIdentity.type, userIdentity.userName

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

eventID, requestID, sourceIPAddress, userIdentity, userIdentity.accessKeyId, userIdentity.arn, userIdentity.principalId, userIdentity.type, userIdentity.userName

Allowlisted first-record sample:

{"eventID":"aws-0001","eventTime":"2026-11-02T12:40:00Z","sourceSystem":"aws-cloudtrail-synthetic","datasetType":"SYNTHETIC","eventName":"GetCallerIdentity","outcome":"SUCCESS","sourceIPAddress":"198.51.100.25"}

### K8S_AUDIT

Source: evidence\kubernetes\kubernetes-audit-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 6

SHA256: 227E4A4A9173635A12566AF5246F3167BDCD968DFD44C9DE6566B9E12DC2F91F

Top-level fields:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

All discovered schema paths:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actorIdentity, containerID, containerName, destinationIP, eventID, podName, podUID, requestID, sourceIP

Allowlisted first-record sample:

{"eventID":"k8s-0001","eventTime":"2026-11-02T12:59:50Z","sourceSystem":"kubernetes-audit-synthetic","datasetType":"SYNTHETIC","action":"get","outcome":"SUCCESS"}

### K8S_FALCO

Source: evidence\kubernetes\falco-runtime-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 4

SHA256: BA61A3976213C45E97316C4E1D22FFD77C17678E4B812C8CE60DDE13A4B30760

Top-level fields:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

All discovered schema paths:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actorIdentity, containerID, containerName, destinationIP, eventID, podName, podUID, requestID, sourceIP

Allowlisted first-record sample:

{"eventID":"k8s-0002","eventTime":"2026-11-02T13:00:05Z","sourceSystem":"falco-runtime-synthetic","datasetType":"SYNTHETIC","action":"application_process","outcome":"OBSERVED"}

### K8S_NETWORK

Source: evidence\kubernetes\network-flow-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 2

SHA256: B8EDA9594E2765A1479F900A8B383B352F3721C7D0B333F0C6DD342DFD6577CA

Top-level fields:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

All discovered schema paths:

action, actorIdentity, cluster, containerID, containerName, datasetType, deployment, destinationIP, destinationPort, eventID, eventTime, filePath, namespace, outcome, parentProcess, podName, podUID, processName, requestID, ruleName, serviceAccount, sourceIP, sourceSystem, statusCode, targetResource

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actorIdentity, containerID, containerName, destinationIP, eventID, podName, podUID, requestID, sourceIP

Allowlisted first-record sample:

{"eventID":"k8s-0003","eventTime":"2026-11-02T13:01:00Z","sourceSystem":"network-flow-synthetic","datasetType":"SYNTHETIC","action":"outbound_connection","outcome":"ALLOWED","sourceIP":"10.244.0.19","destinationIP":"192.0.2.200"}

### LINUX_AUTH

Source: evidence\linux\linux-auth-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 9

SHA256: 71B513E1ED147187C8396591C1782E8A4215F14D4C6753B82FDB6EA7D89F3AAD

Top-level fields:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

All discovered schema paths:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actor, destinationIp, eventId, processId, sessionId, sourceIp

Allowlisted first-record sample:

{"eventID":"lin-0001","eventTime":"2026-11-02T12:50:00Z","sourceSystem":"linux-synthetic","datasetType":"SYNTHETIC_LABORATORY_DATA","action":"ssh.accepted","category":"authentication","outcome":"SUCCESS","sourceIP":"198.51.100.60","destinationIP":""}

### LINUX_PROCESS

Source: evidence\linux\linux-process-persistence-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 6

SHA256: CBBE9708903F19FF8BA8CC495BDBC0A15441CFD8CB92D58C899F6A7F9E40A1A3

Top-level fields:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

All discovered schema paths:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actor, destinationIp, eventId, processId, sessionId, sourceIp

Allowlisted first-record sample:

{"eventID":"lin-0010","eventTime":"2026-11-02T12:50:12Z","sourceSystem":"linux-synthetic","datasetType":"SYNTHETIC_LABORATORY_DATA","action":"process.started","category":"process","outcome":"SUCCESS","sourceIP":"","destinationIP":""}

### LINUX_NETWORK

Source: evidence\linux\linux-network-synthetic.jsonl

Classification: SYNTHETIC_SOURCE_DATA

Records: 3

SHA256: 5FFDA3A5C614C0E53C10B5BA33EBAF875BF4FC58F9685775184CDE67E14044C5

Top-level fields:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

All discovered schema paths:

action, actor, category, datasetType, destinationIp, detail, eventId, eventTime, hostName, outcome, processId, sessionId, sourceIp, sourceSystem, target

Candidate timestamp fields:

eventTime

Candidate identity and attribution fields:

actor, destinationIp, eventId, processId, sessionId, sourceIp

Allowlisted first-record sample:

{"eventID":"lin-0016","eventTime":"2026-11-02T12:50:21Z","sourceSystem":"linux-synthetic","datasetType":"SYNTHETIC_LABORATORY_DATA","action":"tcp.connect","category":"network","outcome":"ALLOWED","sourceIP":"","destinationIP":"192.0.2.40"}

## Correlation Design Requirements

The Python correlation engine must:

1. Parse all seven original JSONL files.
2. Validate event identifiers and timestamps.
3. Preserve source provenance and original event IDs.
4. Normalize UTC timestamps without rewriting sources.
5. Keep network, identity, and process relationships separate.
6. Identify temporal and shared-IP associations.
7. Avoid treating shared IP addresses as proof of causation.
8. Distinguish suspicious events from benign controls.
9. Distinguish synthetic observations from live-lab tests.
10. Return explicit uncertainty and evidence references.

## Limitations

Schema fields alone do not prove relationships.
Source timestamps may use different field names.
Multiple datasets may contain different event structures.

The cross-system correlation engine has not yet
been implemented or tested.

No real AWS, Linux, or Kubernetes incident
was established by this schema audit.

No Kubernetes, Helm, Docker, or AWS resources
were modified.