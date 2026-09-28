# Ticket #008 - Authentication Scenario Design

## Purpose

Define the legitimate and suspicious authentication behaviors that will be represented in the lab dataset before any detector is implemented or tuned.

The scenarios are intentionally mixed so that:

- failed authentication does not automatically mean malicious activity;
- unfamiliar sources do not automatically mean malicious activity;
- familiar sources do not automatically mean benign activity;
- individual events may not reveal the correct security conclusion;
- some benign behavior looks suspicious;
- some suspicious behavior looks relatively ordinary.

## Dataset Target

Target dataset size: approximately 1,000 authentication events.

Events will occur across different:

- users;
- account types;
- source systems;
- source familiarity states;
- times of day;
- authentication outcomes;
- behavioral patterns.

Ground truth will be stored separately from the operational authentication telemetry so the detector cannot use the answer when making its decision.

---

# Legitimate Scenarios

## LEG-01 - Normal Business Authentication

Classification: Benign

Planned events: 600

Behavior:

- normal employee authentication during business hours;
- primarily successful authentication;
- familiar internal workstations;
- multiple ordinary users;
- activity spread throughout the workday.

Purpose:

Provide realistic background authentication volume so suspicious activity is mixed into normal activity rather than isolated.

---

## LEG-02 - Ordinary Password Mistakes

Classification: Benign

Planned events: 90

Behavior:

- users mistype passwords;
- approximately two failed attempts followed by a successful login;
- familiar employee workstations;
- activity distributed across multiple users.

Approximate composition:

- 60 failures;
- 30 successes.

Purpose:

Represent routine user behavior capable of triggering an overly sensitive failure detector.

---

## LEG-03 - Stale Service Credentials

Classification: Benign but operationally noisy

Planned events: 72

Behavior:

- service account attempts authentication repeatedly;
- familiar application server;
- stored password is temporarily outdated;
- failed authentication occurs repeatedly at a regular interval;
- activity continues for several hours.

Purpose:

Create a benign pattern that can strongly resemble automated malicious authentication.

Important:

This scenario must not automatically be excluded simply because it is known service activity. Its security implications must still be evaluated.

---

## LEG-04 - Benign Unfamiliar Source

Classification: Benign

Planned events: 48

Behavior:

- legitimate users authenticate through unfamiliar external sources;
- activity represents remote work or travel;
- primarily successful authentication;
- several ordinary password mistakes are included;
- source addresses are not part of the normal familiar-source baseline.

Approximate composition:

- 40 successes;
- 8 failures.

Purpose:

Demonstrate that an unfamiliar source is context, not proof of malicious activity.

---

## LEG-05 - Legitimate Privileged Administration

Classification: Benign but higher risk

Planned events: 45

Behavior:

- privileged administrator account;
- familiar administrative jump host;
- expected administrative hours;
- primarily successful authentication;
- several ordinary failures are included.

Approximate composition:

- 40 successes;
- 5 failures.

Purpose:

Ensure privileged-account activity remains visible without assuming every privileged authentication is an attack.

---

# Suspicious Scenarios

## SUS-01 - Concentrated Brute-Force Activity

Classification: Suspicious

Planned events: 35

Behavior:

- one unfamiliar source;
- repeated failed authentication against one ordinary user;
- rapid activity within a short period;
- no successful authentication.

Purpose:

Represent a conventional repeated-password attack.

---

## SUS-02 - Failures Followed by Privileged Success

Classification: Suspicious

Planned events: 9

Behavior:

- privileged account;
- unfamiliar source;
- activity occurs around 02:13;
- eight failed authentications;
- followed by one successful authentication.

Purpose:

Represent a high-risk authentication sequence where the success may be more important than the failures.

---

## SUS-03 - Distributed Password Spray

Classification: Suspicious

Planned events: 60

Behavior:

- multiple unfamiliar sources;
- authentication failures distributed across approximately 30 users;
- only a small number of failures against each individual account;
- activity spread sufficiently to avoid looking like a simple brute-force burst.

Purpose:

Represent suspicious behavior that can look relatively ordinary when each user or source is viewed separately.

---

## SUS-04 - Low-and-Slow Authentication Attack

Classification: Suspicious

Planned events: 18

Behavior:

- repeated failures from the same source;
- activity spread across approximately six hours;
- individual time windows contain relatively few attempts;
- target includes a higher-risk account.

Purpose:

Test whether the detector depends too heavily on short time-window thresholds.

---

## SUS-05 - Compromised Familiar Source

Classification: Suspicious

Planned events: 13

Behavior:

- authentication originates from a source considered familiar;
- repeated failures against a sensitive user account;
- failures are followed by a successful authentication.

Approximate composition:

- 12 failures;
- 1 success.

Purpose:

Demonstrate that familiar infrastructure cannot automatically be treated as safe.

---

## SUS-06 - Distributed Attack Against One Account

Classification: Suspicious

Planned events: 10

Behavior:

- one target account;
- failures originate from multiple sources;
- each source generates only a small number of attempts;
- combined behavior is more suspicious than any single source.

Purpose:

Test whether entity aggregation affects detection effectiveness.

---

# Planned Dataset Composition

Benign events: approximately 855

Suspicious events: approximately 145

Total: approximately 1,000 authentication events.

The high percentage of benign activity is intentional. The dataset should resemble an operational environment where most authentication activity is legitimate.

---

# Required Characteristics Coverage

Ordinary user mistakes:
LEG-02

Repeated authentication failures:
LEG-03, SUS-01, SUS-04

Successful authentication:
LEG-01, LEG-02, LEG-04, LEG-05, SUS-02, SUS-05

Known or familiar sources:
LEG-01, LEG-02, LEG-03, LEG-05, SUS-05

Unfamiliar sources:
LEG-04, SUS-01, SUS-02, SUS-03, SUS-04, SUS-06

Privileged or higher-risk accounts:
LEG-05, SUS-02, SUS-04

Different times:
Business-hour and overnight scenarios

Repeated behavior from the same source:
LEG-03, SUS-01, SUS-04

Distributed behavior:
SUS-03, SUS-06

Benign behavior capable of looking suspicious:
LEG-03

Suspicious behavior capable of looking relatively ordinary:
SUS-03

Familiar source containing malicious behavior:
SUS-05

Unfamiliar source containing legitimate behavior:
LEG-04

---

# Ground-Truth Separation

The generated authentication event dataset will contain operational fields required for detection.

Ground-truth classifications will be maintained separately for evaluation.

The detection logic must not use:

- benign/suspicious labels;
- expected outcome;
- scenario classification;
- analyst disposition.

Those fields are evaluation data, not detection telemetry.

---

# Current Status

Scenario design established before dataset generation.

No authentication dataset has been generated.

No detector has been implemented.

No tuning has been performed.
