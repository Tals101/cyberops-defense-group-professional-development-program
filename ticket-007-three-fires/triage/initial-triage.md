# Ticket #007 — Initial Triage Assessment

## Issue A — Privileged SSH Login

**Known Facts:** Successful sysadmin SSH login to APP-PROD-02 from an unfamiliar internal IP. No failed-login burst, maintenance, or related alerts.

**Unknowns:** Who owns the source IP, whether the login was authorized, whether the session is active, and what actions occurred.

**Security Impact:** Possible privileged compromise, persistence, lateral movement, or data access.

**Business Impact:** APP-PROD-02 supports an internal business application; containment could disrupt operations.

**Time Sensitivity:** High if the login is malicious.

**Reversibility:** Account/session containment is reversible but could affect production.

**Confidence:** Low to moderate.

---

## Issue B — Suspicious PowerShell

**Known Facts:** Word launched encoded PowerShell on HR-LT-44. EDR blocked one child process. The workstation remains online.

**Unknowns:** Command contents, originating document, blocked process, network activity, persistence, and whether other actions succeeded.

**Security Impact:** Possible malware execution, credential theft, persistence, or lateral movement.

**Business Impact:** Immediate containment mainly affects one HR user.

**Time Sensitivity:** High because the workstation remains online.

**Reversibility:** Endpoint isolation is easy to reverse.

**Confidence:** Moderate to high that immediate investigation is warranted.

---

## Issue C — Internet Portal Errors

**Known Facts:** Customer errors increased after a recent configuration change. Unusual web requests also increased.

**Unknowns:** Whether traffic is malicious, whether the change caused the errors, and whether rollback restores service.

**Security Impact:** Possible exploitation, scanning, or denial-of-service activity.

**Business Impact:** Active customer-facing service degradation.

**Time Sensitivity:** High operationally, but Operations is already engaged.

**Reversibility:** Configuration rollback should be relatively reversible.

**Confidence:** Low that this is currently a security incident.

---

# Priority Decision

1. **Issue B — Investigate first**
2. **Issue A — Investigate second**
3. **Issue C — Investigate third**

Issue B comes first because it contains multiple suspicious behaviors and the endpoint remains online.

Issue A is second because privileged production access could be serious, but the current evidence is more ambiguous.

Issue C is third for my direct investigation because Operations is already responding and a recent configuration change provides a credible explanation.

---

# Delegation

**Issue A:** Ask the SOC analyst to identify the source IP owner, verify whether the login was expected, and check for related alerts.

**Issue C:** Ask IT Operations to preserve logs, compare deployment timing with the errors, review unusual requests, and prepare rollback.

---

# Five-Minute Rule

**Issue B:** Review the EDR process tree and decode the PowerShell command.  
**Value:** Determines whether immediate isolation is justified.

**Issue A:** Identify the source IP and verify authorization.  
**Value:** Quickly separates legitimate administration from possible compromise.

**Issue C:** Compare deployment timing with the error spike and sample unusual requests.  
**Value:** Helps distinguish operational failure from malicious activity.
