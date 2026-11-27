# Ticket 011 Diagrams

*Added November 27, 2026, after the ticket's technical work was completed. This file is a summary, not part of the original evidence, and is not listed in the ticket's manifests.*

This diagram summarizes the [Ticket 011 README](README.md) and its incident report. It is kept in a separate file because the README is listed in the ticket's submission evidence manifest.

## How the Three Evidence Sources Were Correlated

```mermaid
flowchart LR
    subgraph src["Synthetic evidence sources"]
        AWS["AWS CloudTrail<br/>identity and S3 activity"]
        K8S["Kubernetes<br/>runtime and workload events"]
        LNX["Linux host<br/>authentication and persistence"]
    end
    CE["Python correlation engine<br/>(unit-tested)"]
    TL["42 events in one<br/>UTC timeline"]
    REL["2 shared IP addresses<br/>37 cross-system event pairs"]
    OUT["Relationship possible,<br/>causation not established"]
    FR["2 custom Falco rules<br/>passed positive and<br/>negative controls"]
    AWS & K8S & LNX --> CE --> TL --> REL --> OUT
    K8S --> FR
```

Shared IPs and close timestamps were treated as leads, not proof: the ticket's rule is not to infer causation from timestamps alone. Technical review acceptance and formal closure are still pending.
