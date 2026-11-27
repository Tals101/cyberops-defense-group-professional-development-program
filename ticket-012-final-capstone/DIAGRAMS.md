# Ticket 012 Diagrams

*Added November 27, 2026, after the ticket's technical work was completed. This file is a summary, not part of the original evidence, and is not listed in the ticket's manifests.*

These visuals summarize the [Ticket 012 README](README.md), the laboratory files in [`02-Laboratory/`](02-Laboratory/) and the closure report. They are kept in a separate file because the README is listed in the ticket's final evidence manifest.

## The Simulated Incident

The `application-api` Deployment was changed so its `INTERNAL_URL` pointed at `unapproved-collector` instead of the approved `internal-service`:

```mermaid
flowchart LR
    subgraph ns["Minikube namespace ticket-012-lab"]
        API["application-api<br/>service account<br/>ticket012-application-api"]
        INT["internal-service:8080<br/>approved destination"]
        COL["unapproved-collector:8080<br/>not approved"]
        NP["Deny-all egress<br/>NetworkPolicy"]
    end
    API -- "before: INTERNAL_URL" --> INT
    API -. "after deployment change" .-> COL
    NP -. "not enforced by the<br/>bridge-based CNI" .-> API
```

Two explanations were tested: a deployment automation mistake and an unauthorized change. Because the egress NetworkPolicy was not enforced, the production recommendation is NO-GO.

## Detector Results

![Detector results on 24 labeled synthetic cases](images/detector-comparison.png)

Version 2 detected all 12 suspicious cases but raised 5 false positives on the 12 benign ones (recall 100%, precision 70.6%). Source: [`06-Closure/final-incident-engineering-report.md`](06-Closure/final-incident-engineering-report.md).
