# Ticket 012 — Adversarial / Resilience Test Matrix

**Evidence:** `04-Adversarial-Validation/evidence/adversarial-validation-results.json` and `adversarial-validation-report.txt`. Executable setup: `04-Adversarial-Validation/run_adversarial_validation.py`.

Eight synthetic detector-level scenarios were executed; **8/8 checks matched their expected detector behavior**. A passed *behavioral check* is not necessarily a correct security classification. AV02 was a **false positive**. Exact input, per-case expected fields and observed results are in the machine-readable evidence and test script; the matrix below summarizes those records without claiming real attacker activity.

| Case | Hypothesis and setup | Expected behavior | Observed / supporting evidence | Disposition |
|---|---|---|---|---|
| AV01 | Unapproved network destination combined with deployment/identity indicators | Suspicious alert | Detector scenario assertion matched; case record in JSON | PASS (synthetic) |
| AV02 | Benign identity lookalike resembles suspicious activity | Test detector response and false-positive behavior | Alert on labeled benign case; assertion matched | FALSE POSITIVE; tune |
| AV03 | Clock skew / timestamp ordering challenges change correlation | Correct timing classification | Scenario assertion matched; JSON results | PASS; timing caveat |
| AV04 | Identity field missing or ambiguous | Do not claim verified attribution; handle missing data | Scenario assertion matched; JSON results | PASS; attribution gap |
| AV05 | Configuration change affects network-event interpretation | Evaluate deployment/configuration context | Scenario assertion matched; JSON results | PASS (synthetic) |
| AV06 | Deployment telemetry unavailable | Preserve missing-telemetry limitation | Scenario assertion matched; JSON results | PASS; incomplete evidence |
| AV07 | Policy misconfiguration permits bypass | Execute synthetic detector test; review operational policy test separately | Synthetic check passed; actual deny-all egress policy did **not** block collector | DETECTOR PASS; NETWORK CONTROL FAIL |
| AV08 | Failed/incomplete rollback must be detected | Synthetic resilience check; operational recovery separately | Synthetic check passed; operational bad image reached ImagePullBackOff, invalid revision failed, valid undo succeeded | PASS for expected checks; not real rollback-engine failure |

## Separate operational tests

- Application direct connection to unapproved collector remained possible with the tested CNI (`networkpolicy-enforcement-test.txt`).
- Scaling the collector to zero removed its reachability; approved application flow remained functional; collector restored to one ready replica (`containment-restoration-results.txt`).
- A disposable rollback probe experienced `ImagePullBackOff`; rollback to nonexistent revision 999 was rejected; normal `rollout undo` restored the known-good image (`rollback-failure-recovery-results.txt`).

**Limitations:** Tests use synthetic inputs, a small labeled dataset and claimed—not cryptographically authenticated—identity metadata. No actual compromise or exfiltration was demonstrated. Production recommendation: **NO-GO**.
