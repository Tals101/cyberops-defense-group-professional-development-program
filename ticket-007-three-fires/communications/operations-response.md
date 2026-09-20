# Response to Operations — Portal Rollback

I can confirm intermittent HTTP 500 responses and unusual requests in the portal evidence, but I cannot link those requests to the failures. The recent configuration deployment is still a plausible explanation. Please preserve the web, application, and configuration logs, with timestamps and examples of the unusual requests, then proceed with the known-good rollback. Security does not need to hold up restoration on the evidence we have.

I will continue reviewing the traffic separately. Let me know the portal's response after rollback; we should reassess immediately if errors persist or a successful exploit becomes visible. At this stage, the unusual requests may be unrelated scanning rather than the cause of the outage.
