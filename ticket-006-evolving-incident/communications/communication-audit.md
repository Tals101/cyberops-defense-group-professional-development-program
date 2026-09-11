# Ticket #006 — Communication Audit

| Communication | What I Believed Then | Confidence | What Later Changed |
|---|---|---|---|
| 09:30 | Unusual outbound HTTPS activity from FIN-WS17 was confirmed, but the destination, initiating process, data transferred, and maliciousness were not yet established. Both legitimate activity and compromise remained plausible. Continued monitoring without immediate disruption was appropriate. | Low-to-medium regarding compromise; high regarding the existence of unusual outbound activity. | Later investigation identified the processes involved, confirmed Finance-file transmission, and established that an additional non-standard utility was responsible for the concerning transfer. |
| 10:15 | Two Finance files had been transmitted externally through a process not documented as the normal Finance workflow. The destination infrastructure also supported legitimate organizations. There was insufficient evidence to conclude full compromise or attribute malicious intent to Mark. Targeted containment and increased monitoring were preferred over full isolation. | High that data was transferred; medium-high that the additional utility was unauthorized; low regarding actor intent and broader compromise. | At 11:00, recurring activity from the same recently introduced non-standard process materially increased risk and justified full network containment. At 11:40, Security learned that Mark had installed the utility after receiving a purported vendor email. |
| 11:10 | Repeated communications from a recently introduced non-standard process, combined with confirmed Finance-file transmission, justified treating the matter as a security incident and isolating FIN-WS17. The installer and reason for installation were still unknown. | High that a security-impacting data transfer occurred; medium-high that containment was justified; low regarding root cause and malware status. | At 11:40, the employee was identified as the installer and explained that he believed the software came from a known vendor for data conversion. Later static and server analysis showed that the observed utility performed no conversion and instead transmitted Finance data externally. |

## Did Any Earlier Statement Become Incorrect After Later Evidence Emerged?

Yes, one statement became outdated after new evidence emerged.

At 11:10, Communication #3 stated that Security did not know who installed the software or why. At 11:40, later evidence established that Mark installed it after receiving a link represented as coming from a known Finance vendor and believed it was needed for financial-data conversion.

The 11:10 statement was nevertheless reasonable and accurate when it was made because that information had not yet been established.

Communication #2 also stated that Security had not concluded that Mark caused the activity. Later evidence established that Mark installed the utility, but it did not establish that he knowingly intended to transmit Finance data or cause a security incident. Therefore, the earlier statement was appropriately cautious rather than incorrect.

Communication #1 did not become incorrect. Its uncertainty reflected the limited evidence available at 09:30, and later findings appropriately resolved several of those unknowns.

## Communication Quality Assessment

The communications became progressively more decisive as evidence increased:

- 09:30 — elevated but unconfirmed risk; preserve evidence and avoid premature disruption.
- 10:15 — confirmed data transfer but unresolved intent and authorization; targeted containment.
- 11:10 — recurring non-standard activity plus confirmed data transfer; classify as an incident and isolate the workstation.

The changing recommendations reflect new evidence rather than contradiction.
