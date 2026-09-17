# Ticket #007 — Stakeholder Map

## SOC
**Involved:** Yes

**Why:** Owns alert triage, evidence collection, environment-wide IOC searching, and ongoing monitoring.

## IT Operations
**Involved:** Yes

**Why:** Supports endpoint restoration, operational coordination, and follow-up for Issue C. Also owns the maintenance-process correction for Issue A.

## HR
**Involved:** Yes

**Why:** HR-LT-44 is assigned to an HR employee and may contain sensitive employee information. HR should coordinate user impact and help determine data sensitivity.

## Management
**Involved:** Yes

**Why:** Management needs incident status, business impact, scope, resource needs, and escalation decisions.

## Identity / IAM
**Involved:** Yes

**Why:** Review the HR user's authentication activity and determine whether credentials or tokens may have been misused.

## Network Engineering
**Involved:** Yes

**Why:** Search for additional communication with the external destination and implement blocking if Security determines it is appropriate.

## Legal / Privacy
**Involved:** Conditional

**Why:** Involve if investigation confirms or reasonably indicates unauthorized access to sensitive employee or regulated data.

## Communications
**Involved:** Not currently.

**Why:** There is no confirmed external disclosure or public-facing security impact requiring communications support at this time.

## Vendor Management
**Involved:** Not currently.

**Why:** No vendor has been identified as contributing to or requiring action for the confirmed incident.

## Email / Messaging Administration
**Involved:** Yes

**Why:** Search for the suspicious message across mailboxes, preserve headers and attachment evidence, identify additional recipients, and support message removal if required.

## Endpoint / Desktop Support
**Involved:** Yes

**Why:** Maintain HR-LT-44 containment and perform remediation or reimaging after Security completes evidence preservation.
