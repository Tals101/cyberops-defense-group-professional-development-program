# Ticket #003 - Lessons Learned

## 1. What did the first detection get wrong?

My first version put too much weight on the number of failures. If the same account received five failed SSH passwords from one source within two minutes, the detector alerted. That worked against the Kali test, but the false-positive exercise showed that a real user could create the same pattern simply by entering the wrong password several times.

The missing piece was context. Version 1 did not know whether the source was normal for the account or whether the user successfully logged in right after the failures.

## 2. What evidence led to the change?

The strongest evidence came from the legitimate retry test. From the normal Windows source at `192.168.56.1`, I generated five failed passwords and then completed a successful login. Version 1 still produced an alert.

That test made the problem easy to see: the count and timing looked suspicious, but the surrounding behavior pointed toward user error.

## 3. Which legitimate behavior was hardest to separate from suspicious activity?

Repeated password mistakes were the hardest case. A frustrated user can retry quickly several times, which can look almost identical to a short password-guessing attempt if the detector only looks at failures.

The successful login that followed helped, but I did not want to treat success by itself as proof that everything was safe. Source familiarity had to be part of the decision too.

## 4. What tradeoff did you make between sensitivity and false positives?

I used five failures within two minutes rather than alerting on one or two mistakes. That choice reduces noise from ordinary login errors, but it also means a slow attacker could stay below the threshold.

Version 2 makes another tradeoff by suppressing the high-priority alert when the failures come from a known source and are followed by a successful login. That reduces the specific false positive I observed, while accepting that the rule needs more context before it would be appropriate for production.

## 5. What would you change before using this in a production SOC?

I would replace the static source list with historical login baselines and add richer identity and endpoint context. Useful fields would include:

- Device identity
- Account privilege
- MFA status
- Asset criticality
- Geolocation
- Source reputation
- Historical login patterns
- Multiple accounts targeted by one source
- Multiple sources targeting one account
- Successful authentication after failures
- Related authentication activity across other endpoints

I would also run the detector against a much larger dataset, measure alert volume, and tune severity before enabling high-priority notifications.
