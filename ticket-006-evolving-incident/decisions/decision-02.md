# Ticket #006 — Decision Point #2

## 11:00 Reassessment

### 1. What Is Now Established as Fact?

Based on the evidence collected in earlier phases and the new 11:00 telemetry:

- FIN-WS17 has generated repeated outbound network connections at regular intervals.
- The same process is responsible for each of the newly observed recurring connections.
- The responsible process is not part of the standard operating system installation.
- The associated file was introduced recently.
- The mreynolds user account had an interactive session during the relevant timeframe.
- Endpoint security tooling has not classified the file as malicious.
- The reason the software was installed is not known.
- Earlier investigation confirmed that Finance files were packaged and transmitted externally.
- The previously observed Finance-file transfer was successful.
- The external infrastructure is used by legitimate organizations but has also previously been abused by threat actors.
- FIN-WS17 remains operational.

The new telemetry establishes recurrence and consistency of the process behavior. It does not, by itself, establish who installed the software or why.

### 2. What Remains Inference?

The following conclusions are supported by the evidence but are not yet proven facts:

- The recurring process may be performing unauthorized activity.
- The regular connection interval may represent automated beaconing or scheduled data transfer.
- The recently introduced file may have been installed specifically to enable the observed outbound activity.
- The process may be related to the previously confirmed Finance-file transfer.
- The use of non-standard software and repeated communications may indicate persistence or attacker-controlled automation.
- The interactive user session may be related to installation or execution of the software.

None of these points establish who installed the software, whether mreynolds intentionally used it, or whether an external attacker controls the process.

The absence of an antivirus detection does not establish that the software is safe. It only establishes that the available endpoint tooling has not classified it as malicious.

### 3. What Remains Unknown?

The following questions are still unresolved:

- Who installed or introduced the recurring process?
- Why was the software installed?
- Whether the software was approved by Finance, IT, or Security.
- Whether mreynolds intentionally launched or used the software.
- Whether the process is controlled by an external actor.
- Whether each recurring connection transfers data, receives commands, or performs another function.
- Whether additional Finance files or credentials have been accessed.
- Whether the process has affected other systems.
- Whether there are persistence mechanisms not yet identified.
- Whether the external destination is specifically authorized for this workstation.
- Whether the process is related to legitimate business automation that is missing from the documented baseline.
- Whether the workstation has experienced a broader compromise beyond the observed process activity.

### 4. Has the Risk Changed?

Yes.

The risk has increased from High to Critical.

The earlier investigation established a confirmed external transfer of Finance data through document_cache.sh. The 11:00 telemetry now adds:

- Regular recurring outbound connections.
- The same process responsible for each connection.
- A process that is not part of the standard operating system.
- A file that was introduced recently.
- Continued activity during an interactive user session.
- An unresolved installation purpose.

These facts increase the likelihood that the observed behavior is persistent, automated, or otherwise continuing rather than an isolated unexplained transfer.

The lack of antivirus classification reduces certainty about malware but does not materially reduce the risk created by the observed behavior.

### 5. Has the Recommended Action Changed?

Yes.

The recommended action has changed from targeted containment with continued Finance operation to full network containment of FIN-WS17.

### 6. What Evidence Caused the Change?

The recommendation changed because the evidence now establishes:

- Continued recurring communication rather than a single event.
- Consistent use of the same recently introduced non-standard process.
- Prior confirmed transmission of Finance files.
- No established business purpose for the process.
- Continued uncertainty about who introduced or controls the software.

The cumulative evidence now outweighs the operational benefit of keeping FIN-WS17 connected.

## Containment Decision

FIN-WS17 should now be isolated from the network while remaining powered on.

### Rationale

Network isolation is justified because continued connectivity creates an ongoing risk of additional unauthorized data transfer or external control.

The workstation should remain powered on to preserve volatile evidence and allow controlled forensic collection.

### Strongest Argument Against Containment

Finance has time-sensitive reporting requirements, and the workstation remains operational with no user-reported symptoms or antivirus detection.

Isolation will disrupt Mark's work and may delay Finance deliverables.

### Why Containment Is Still Defensible

The decision is not based on antivirus status or destination reputation.

It is based on the combination of:

- Confirmed Finance-file transfer.
- Repeated communications.
- A recently introduced non-standard process.
- Unknown software purpose.
- Continued activity.
- Lack of established authorization.

The security risk of allowing further external communication now exceeds the operational risk of temporarily disconnecting the workstation.

### Conditions for Reconnection

FIN-WS17 should remain isolated until:

- The recurring process is identified and its purpose is validated.
- The process is confirmed authorized or removed.
- The workstation is assessed for broader compromise.
- Relevant credentials and sensitive-data exposure are evaluated.
- Security determines that reconnecting the system does not create unacceptable risk.
