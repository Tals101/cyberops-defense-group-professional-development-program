# Ticket #008 — Decision Point #1
## SOC Manager Recommendation — Familiar Internal Address Suppression

I do not recommend blanket suppression of alerts from familiar internal addresses.

On the current V1 dataset, the exception would likely reduce alert volume from 15 to 12. However, only one removed alert would be known benign service-account activity; two would suppress the SUS-05 compromised familiar-source scenario. Scenario coverage would therefore fall from 6/6 to 5/6.

The request assumes that internal means trusted and familiar means benign. Neither assumption is reliable. A compromised workstation, stolen credentials, lateral movement, or an attacker using an established internal host can generate malicious activity from a familiar address.

A narrower alternative is to preserve familiar-source visibility while further correlating repetitive activity into investigation-level cases. Stable service failures can remain grouped, and related alerts from the same authentication sequence or campaign can be consolidated without excluding the source itself.

Recommendation: reject blanket familiar-address suppression and pursue correlation-based V2 tuning instead.
