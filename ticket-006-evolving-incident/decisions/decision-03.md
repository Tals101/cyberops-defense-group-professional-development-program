# Ticket #006 — Decision Point #3

## 12:30 Business Pressure

Finance reports that Mark's converted files are needed within the next two hours or today's reporting deadline may be missed.

Security has not yet reached a definitive conclusion about whether the software is malicious.

## Recommendation Right Now

### Workstation Risk

FIN-WS17 should remain network isolated and powered on.

It should not be returned to normal Finance use at this time.

The reason is not simply that the software is unsigned or unapproved. The decision is based on the cumulative evidence:

- Finance data was confirmed to have been transmitted externally.
- The responsible software was recently introduced.
- The software is not part of the standard operating system.
- The software was not deployed by IT or approved by Security.
- Its observable behavior does not match the stated data-conversion purpose.
- The client packages and transmits Finance files.
- The external server stores the transmitted data but performs no observed conversion.
- The external service identity has not been independently verified.
- The original vendor email and download source have not been independently authenticated.

The workstation should remain available for forensic examination while isolated from external communication.

### Business Continuity

Finance should continue legitimate work using a clean, trusted workstation or other approved corporate system.

Required business files should be recovered from a known-good source where possible, such as an approved file share, backup, document repository, or another trusted Finance system.

If files must be recovered from FIN-WS17:

1. Identify only the specific business files required for today's report.
2. Copy them using a controlled process approved by Security or IT.
3. Scan and validate the files before placing them on the clean system.
4. Do not transfer document_cache.sh, unknown executables, scripts, temporary archives, or other unverified software.
5. Preserve original evidence on FIN-WS17.

The required data conversion should be performed using:

- An existing approved corporate application;
- A known-good conversion utility supplied and verified by IT;
- A trusted manual or alternate workflow; or
- A vendor-provided method only after the vendor and software are independently validated through a known contact channel.

Security should contact the known Finance vendor using previously established contact information rather than replying to the questionable email or using contact information from the download site.

## Business Impact

Keeping FIN-WS17 isolated may delay Mark's normal workflow.

Providing a clean workstation and an approved conversion path gives Finance a reasonable opportunity to meet the reporting deadline without restoring a potentially unsafe system to the network.

## Security Impact

This approach prevents additional observed transfer behavior while preserving evidence and allowing the investigation to continue.

It also avoids unnecessarily blocking the entire Finance function.

## Decision

Maintain containment of FIN-WS17.

Provide Finance with a clean-system business-continuity workflow immediately.

Do not reconnect FIN-WS17 solely to meet the reporting deadline.

## What Would Change This Decision

Reconnection could be reconsidered if independent evidence establishes that:

- The vendor sent the original message.
- The download location belongs to the vendor.
- The software is authentic and matches a vendor-verified copy.
- The observed external transfer is an expected and authorized component of the business process.
- Security determines that continued operation presents acceptable risk.

Until those conditions are met, business continuity should occur on a separate trusted system.
