# Issue C — Customer Portal Error Spike

**Disposition: Operational Issue with Security Follow-Up**

## Basis for the decision

The portal returned intermittent HTTP 500 responses after a configuration deployment. Unusual requests were also present, but a recorded error preceded the suspicious requests in the sample. After Operations restored the prior configuration, errors moved quickly toward baseline even though the unusual requests continued.

That sequence supports a configuration-related availability problem more strongly than a traffic-driven outage. It does not prove that every unusual request was harmless or that no attempted exploit occurred.

**Confidence:** Moderate to high that the service errors were primarily operational; no successful portal compromise was confirmed.

## Impact and follow-through

The immediate business impact was degraded customer access and likely additional support demand. Security preserved the relevant logs, reviewed request/error timing, and advised Operations to proceed with restoration rather than wait for a completed security investigation.

IT Operations owns stable service. The SOC should continue reviewing the unusual traffic and escalate if it finds exploit evidence or abnormal application behavior.

**Closure condition:** The portal remains stable after rollback, and the follow-up traffic review identifies no successful exploitation requiring further action.
