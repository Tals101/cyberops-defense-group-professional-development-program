# V3 Adversarial Automation Test Plan

## Purpose

Test whether an attacker who can manipulate trusted automation inputs could cause V3 to grant unsafe remediation authority.

All testing is synthetic and isolated from production systems.

## Test Principles

Each adversarial test will answer:

1. What trusted input is manipulated?
2. What unsafe outcome is the attacker attempting to cause?
3. Does V3 detect or block the manipulation?
4. If not, what control is missing?
5. What authority should the automation retain after the finding?

---

## A01 — Secondary Evidence Poisoning

### Attack

Manipulate the secondary corroboration record for `payroll.emergency` so that it falsely agrees with the incorrect primary IAM record.

The attacker will attempt to change secondary context from:

- integration identity;
- active lifecycle;
- critical business importance;
- Emergency Payroll Integration dependency;

to a benign-looking workforce identity with:

- employee role;
- inactive lifecycle;
- low business criticality;
- no application dependency.

### Attacker Goal

Turn conflicting evidence into apparently trusted corroboration and cause the V3 engine to elevate authority from:

`REQUIRE_APPROVAL`

to:

`AUTO_REMEDIATE`

### Security Question

Can an attacker defeat corroboration by poisoning one supposedly independent trusted source?

### Expected Safe Behavior

V3 should ideally detect loss of source integrity or provenance and refuse automatic remediation.

If it cannot, this test identifies a trust-boundary weakness requiring source-integrity controls.

---

## A02 — Freshness Metadata Forgery

### Attack

Provide evidence labeled `current` while embedding an observation timestamp showing that the information is actually stale.

### Attacker Goal

Cause the automation to accept old evidence as current by manipulating only the freshness label.

### Security Question

Does V3 independently validate evidence age, or does it trust a source-provided freshness designation?

### Expected Safe Behavior

Evidence age should be calculated from independently verifiable timestamps rather than trusting a simple `current` label.

If the engine ignores contradictory timestamp evidence, the test identifies a freshness-validation weakness.

---

## A03 — Approval Forgery / Replay

### Attack

Present an approval artifact that says `APPROVED` but is not strongly bound to:

- the specific identity;
- the specific requested action;
- the approver;
- the approval timestamp;
- an expiration time;
- a unique request identifier.

### Attacker Goal

Reuse or forge generic approval data to authorize a destructive identity change.

### Security Question

Is approval merely a status value, or is it a validated authorization artifact tied to one specific operation?

### Expected Safe Behavior

Destructive remediation should require a unique, current, operation-specific approval record.

Generic or replayed approval must not authorize execution.

---

## Success Criteria

Adversarial testing is successful when:

- unsafe trust assumptions are identified before production use;
- unsafe actions remain confined to synthetic working copies;
- findings result in explicit safeguards or authority restrictions;
- no discovered weakness is hidden or rewritten as an initial success.

## Evidence Strategy

For each test preserve:

- manipulated input;
- test harness;
- decision or execution output;
- observed unsafe or safe behavior;
- finding;
- corrective control if required;
- retest evidence where applicable.

## Production Constraint

Until adversarial testing and least-privilege analysis are complete:

**Full unattended destructive identity remediation remains prohibited.**
