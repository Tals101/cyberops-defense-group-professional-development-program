# Ticket #006 — Lessons Learned

## 1. What did you initially think was happening?

At 09:17, I did not have enough evidence to determine whether the activity was malicious.

My initial hypotheses included:

- Legitimate Finance application activity.
- A legitimate application behaving abnormally.
- Unauthorized data transfer.
- Command-and-control communication.
- A compromised user or application session.

The initial assessment was therefore elevated but unconfirmed rather than a declaration of compromise.

## 2. Which early evidence was most misleading?

The most potentially misleading early evidence was that the external infrastructure was used by many legitimate organizations, the workstation remained operational, the user reported no unusual behavior, and antivirus had not generated an alert.

Those facts could have created false reassurance.

None of them explained the confirmed transfer of Finance data through document_cache.sh, and none proved that the additional software was safe.

## 3. Did you become too confident at any point?

I came closest at 11:00 when the risk rating was raised to Critical and full network containment was recommended.

However, I continued to separate what was known from what was inferred.

I was highly confident that Finance data had been transmitted and that containment was justified, but I remained uncertain about malware status, actor identity, employee intent, and root cause.

The important lesson is that confidence should be attached to specific conclusions rather than to the incident as a whole.

## 4. Which piece of evidence changed your assessment the most?

The assessment materially changed when recurring communications were tied to the same recently introduced non-standard process after Finance data had already been confirmed as transmitted.

Later, the strongest investigative pivot was static and server analysis showing that the supposed conversion utility performed no observed conversion.

Instead, it packaged Finance files, transmitted them externally, and the receiving server stored the data.

That behavior directly conflicted with the purpose represented to the employee.

## 5. Did business pressure affect your technical judgment?

Business pressure influenced the response plan but did not override the evidence.

At 10:15, the reporting requirement supported choosing a less disruptive targeted-containment approach because broader compromise had not yet been established.

By 12:30, the evidence justified continued isolation despite the reporting deadline.

Business impact was addressed through a clean workstation, trusted copies of required files, and an approved conversion method rather than by reconnecting FIN-WS17.

## 6. At what point, if any, did containment become justified?

Full network containment became justified at Decision Point #2 around 11:00.

By then, Security had:

- Confirmed external transmission of Finance data.
- Identified recurring communications.
- Identified the same recently introduced non-standard process as responsible.
- Failed to establish an approved business purpose for that process.

The cumulative evidence showed an ongoing risk that outweighed the operational benefit of leaving FIN-WS17 connected.

## 7. What was the cost of waiting?

The primary cost of waiting was continued exposure.

If the process was unauthorized or malicious, additional Finance data could have been transferred while the workstation remained connected.

Waiting also created the possibility of further external communication or activity that had not yet been identified.

The benefit of the initial measured approach was that Security obtained additional evidence before imposing a disruptive control.

## 8. What would have been the cost of containing too early?

Immediate isolation at 09:17 could have interrupted time-sensitive Finance reporting before Security knew what process was communicating or whether the activity was legitimate.

It could also have unnecessarily disrupted a business-critical employee and reduced cooperation with Finance.

A premature response might have created avoidable operational impact without materially improving the investigation beyond what targeted evidence collection could initially provide.

Powering the system off would also have risked losing volatile evidence, which is why later containment specifically kept the workstation powered on.

## 9. How did your communications change as confidence increased?

The communications became progressively more decisive.

At 09:30, I reported elevated but unconfirmed risk and recommended continued investigation without disrupting Finance.

At 10:15, I reported confirmed Finance-file transfer but maintained uncertainty regarding intent and broader compromise, recommending targeted containment and monitoring.

At 11:10, recurring activity and the recently introduced non-standard process justified calling the matter a security incident and recommending network isolation.

The language became stronger because the evidence became stronger.

## 10. What would you do differently during a real incident?

During a real incident, I would seek independent vendor validation earlier using a known-good contact method.

I would also obtain:

- The original email with complete headers.
- Browser and download history.
- The exact download URL.
- Endpoint process-tree information.
- File reputation and sandbox analysis.
- A vendor-provided known-good file and hash.
- Identity and authentication telemetry.
- Network proxy, DNS, and firewall records.

I would coordinate earlier with IT and Finance to prepare a clean replacement workstation in case containment became necessary.

## 11. What information did management need that engineers did not?

Management primarily needed:

- Whether there was an incident.
- Current business and security risk.
- What Security was doing.
- Whether Finance could continue working.
- Expected operational impact.
- What uncertainty remained.
- What would cause the response to escalate or change.
- What leadership should communicate to stakeholders.

Management did not need every command, hash, packet detail, or process argument in order to make business decisions.

## 12. What information did engineers need that management did not?

Engineers needed detailed technical evidence, including:

- Process execution and parent/child relationships.
- File paths and timestamps.
- SHA-256 hashes.
- Audit logs.
- Packet-capture evidence.
- Network destinations and connection timing.
- Files accessed and transmitted.
- Script contents.
- Server behavior.
- TLS certificate details.
- Persistence checks.
- Email and download provenance.
- Authorization and baseline comparisons.

These details were necessary to test competing hypotheses, reproduce findings, preserve evidence, and support the final classification.

## Overall Lesson

The central lesson from Ticket #006 is that professional incident response requires making defensible decisions before certainty is available.

The correct response is not to force an early yes-or-no conclusion.

It is to clearly state what is known, what remains uncertain, the current level of risk, the action being taken, and the evidence that would cause the decision to change.
