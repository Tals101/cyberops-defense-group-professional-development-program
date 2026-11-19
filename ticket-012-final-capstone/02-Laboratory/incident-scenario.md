# Ticket 012 - Simulated Incident Scenario

## Scenario
An application unexpectedly communicates with a service
that is not on its approved destination list.

## Approved Communication
Source: application-api
Destination: internal-service
Port: 8080
Status: Approved

## Suspicious Communication
Source: application-api
Destination: unapproved-collector
Port: 8080
Status: Not approved

The unapproved destination will exist only inside
the isolated Ticket 012 laboratory.

## Hypothesis 1 - Configuration Error
A deployment automation mistake changed the
application's configured destination.

## Hypothesis 2 - Unauthorized Change
An unauthorized modification redirected application
traffic to an unexpected internal destination.

## Evidence Required
- Kubernetes deployment configurations
- Application logs
- Internal service access logs
- Network destination information
- Identity and authorization information
- Deployment change timestamps

## Investigation Objective
Determine which explanation is supported by the
collected evidence.

## Safety
- Synthetic data only
- Synthetic credentials only
- No external communication targets
- No real data exfiltration
- No changes outside ticket-012-lab

## Current Status
Scenario designed.
Suspicious activity not yet executed.
