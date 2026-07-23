# Ticket 001 Lessons Learned

## Overview

Ticket 001 gave me the opportunity to work through a complete SSH authentication investigation rather than focusing on only one technical task.

The project included log analysis, event correlation, Wazuh alert validation, account containment, network containment, Bash scripting, cron scheduling, evidence preservation, and incident reporting.

The investigation also included several unexpected problems. Those challenges made the project more realistic and helped me identify specific ways to improve my process.

## Start With the Native System Logs

One of the most important lessons was to begin with the logs generated directly by the affected system.

The Ubuntu SSH records provided the clearest view of:

- The targeted account
- The source IP address
- The failed login attempts
- The successful authentication
- The associated session activity

Wazuh was useful as an additional detection and correlation layer, but the investigation did not depend entirely on the SIEM.

This became especially important when the Wazuh agent was temporarily pending or disconnected.

In future investigations, I will continue treating native operating-system logs as a primary evidence source and use centralized monitoring platforms to support and validate those findings.

## Verify Monitoring Before Testing

I initially expected the Wazuh dashboard to display the SSH activity immediately.

When the expected alerts did not appear, I found that the agent was not fully connected.

This taught me that monitoring should be validated before generating test activity.

Before beginning a future detection test, I will confirm:

- The endpoint agent is running
- The agent is connected to the manager
- Logs are being collected
- Events are reaching the monitoring platform
- The expected rules are enabled
- System clocks are synchronized

Taking a few minutes to verify these conditions can prevent confusion later.

## Use More Than One Evidence Source

No single file told the entire story.

I had to compare several records to understand what happened:

- SSH service logs showed the authentication sequence
- `lastb` showed failed login history
- `last` showed successful session history
- File metadata confirmed post-login activity
- Wazuh alerts provided an additional detection layer
- Screenshots preserved the dashboard findings
- Containment records documented the response actions
- Detector output showed that the custom control worked

Correlating these sources gave me more confidence in the final conclusion.

It also made the investigation easier to defend because each major finding was supported by more than one record.

## Preserve Evidence Before Applying Containment

Containment can change the environment.

A firewall block can prevent additional connections, and an account lock can stop further authentication. Those actions may be necessary, but they can also interrupt evidence collection or testing.

During this project, I collected the key authentication and session records before applying the temporary network block.

That sequence helped preserve the original activity before the environment changed.

In a future investigation, I will continue using this general order when it is safe to do so:

1. Confirm the activity.
2. Preserve the important evidence.
3. Record the current state.
4. Apply containment.
5. Verify that containment worked.
6. Document the rollback procedure.
7. Continue monitoring for related activity.

In an urgent production incident, immediate containment may take priority. The decision should be based on the level of risk and the potential impact of waiting.

## Plan the Rollback Before Applying a Control

The temporary nftables rule successfully blocked the source IP address.

However, it also prevented the authorized Kali Linux system from continuing the SSH tests.

The control worked exactly as designed, but I had not fully accounted for how it would affect the remaining lab steps.

This taught me to define the rollback procedure before applying a temporary control.

For future containment actions, I will document:

- The exact command being applied
- The intended result
- The systems that may be affected
- How success will be tested
- The exact rollback command
- Who should approve the change in a production environment

Containment should be controlled, measurable, and reversible whenever possible.

## Automation Needs State

The custom Bash detector correctly identified repeated SSH authentication failures.

However, it searched a rolling time window without remembering which events had already been processed.

As a result, the same activity could generate repeated alerts during later cron executions.

The detector was useful as a proof of concept, but it was not production-ready.

A stronger version should include:

- A state file or database
- A record of the last processed event
- Duplicate-alert suppression
- Configurable thresholds
- Configurable time windows
- Structured output
- Improved error handling
- Automated tests
- Centralized alert delivery

The main lesson was that detecting an event is only one part of building a reliable detection. The detector must also manage repeated executions and alert quality.

## Record the Timeline During the Investigation

I created a technical timeline that connected the failed login attempts, successful authentication, post-login activity, Wazuh alerts, containment, and detector testing.

The timeline was valuable, but it would have been easier to build if I had recorded each major event as it occurred.

Reconstructing a timeline later requires searching through commands, logs, screenshots, and file timestamps.

For future tickets, I will maintain a running investigation record that includes:

- Date and time
- Action performed
- Command used
- System involved
- Expected result
- Actual result
- Evidence filename
- Follow-up action

This will reduce rework and improve the accuracy of the final report.

## Document Problems Instead of Hiding Them

Several parts of the project did not work perfectly on the first attempt:

- The Wazuh agent experienced a connectivity problem
- The firewall rule interrupted authorized testing
- The custom detector produced repeated alerts
- The first `scp` destination path was incorrect
- Some PowerShell path variables had to be recreated

These problems were part of the engineering process.

Documenting them showed:

- What failed
- Why it failed
- How I diagnosed it
- How I corrected it
- What I would do differently next time

A technical portfolio is more useful when it shows realistic troubleshooting rather than presenting every project as if it worked perfectly from the beginning.

## Test File Transfers Before the Final Handoff

The first `scp` transfer failed because the Windows destination path ended with a trailing backslash.

I corrected the problem by changing into the intended destination directory and using `.` as the destination.

This was a small issue, but it could have delayed the final handoff if it had happened at the end of the project.

Before transferring a final evidence package, I should verify:

- The destination directory exists
- The path is quoted correctly
- The account has permission to write there
- The files arrive with the expected names
- The transferred files can be opened
- File hashes still match after transfer

## Evidence Integrity Should Be Repeatable

The final evidence package included an inventory and SHA-256 manifest.

I recalculated every listed hash and confirmed that all 19 validation checks passed.

This provided confidence that the files had not changed after the manifest was generated.

The process worked, but it involved several manual PowerShell commands.

A future improvement would be a single script that:

1. Identifies the evidence files
2. Builds the inventory
3. Calculates the hashes
4. Writes the manifest
5. Validates every hash
6. Reports missing or modified files
7. Exits with a clear success or failure code

This would make evidence validation faster, more consistent, and easier for another engineer to reproduce.

## Separate Lab Actions From Production Recommendations

This project took place in an authorized lab environment.

Some actions were appropriate for the lab but would require additional planning and approval in production.

Examples include:

- Generating repeated failed login attempts
- Using password-based SSH authentication
- Applying a firewall block directly
- Locking an account during active testing
- Running a custom detector through the root crontab

In a production environment, these actions could affect users, services, compliance requirements, or business operations.

Future documentation should clearly distinguish between:

- What was done in the lab
- What would be recommended in production
- What approvals would be required
- What risks would need to be evaluated
- How the change would be monitored and reversed

## Clear Documentation Is Part of the Technical Work

The investigation was not complete when the technical testing ended.

The findings still had to be organized into:

- A weekly README
- An engineering log
- Lessons learned
- A formal incident report
- An architecture diagram
- A technical timeline
- An evidence inventory
- A SHA-256 manifest

Writing the documentation forced me to check whether my conclusions were supported and whether another engineer could follow the investigation.

Good documentation is not separate from technical work. It is how technical work becomes understandable, reviewable, and reusable.

## What Worked Well

Several parts of my approach worked well:

- Starting with native Ubuntu logs
- Correlating multiple evidence sources
- Confirming post-login activity
- Validating Wazuh alerts after reconnecting the agent
- Preserving screenshots and log output
- Testing both account and network containment
- Building a working custom detector
- Scheduling the detector with cron
- Creating a technical timeline
- Generating and validating SHA-256 hashes
- Organizing the project into clear folders
- Using focused Git commits

These practices created a stronger and more complete investigation.

## What I Would Change Next Time

If I repeated Ticket 001, I would:

- Confirm Wazuh connectivity before generating any activity
- Verify log ingestion before expecting dashboard alerts
- Begin the engineering log and timeline immediately
- Automate evidence collection earlier
- Create the rollback command before applying the firewall block
- Add persistent state to the custom detector
- Suppress duplicate alerts
- Produce structured detector output
- Add automated detector tests
- Use one script for inventory creation and hash validation
- Test the final transfer path earlier
- Prepare a short executive summary before writing the full report
- Keep clearer notes about the exact time of each action

## Skills Strengthened

This ticket helped me improve my ability to:

- Investigate SSH authentication activity
- Read and interpret Linux security logs
- Correlate events across multiple sources
- Build a technical timeline
- Validate SIEM alerts
- Troubleshoot monitoring-agent problems
- Apply account containment
- Test network containment
- Write Bash detection logic
- Schedule scripts with cron
- Preserve evidence
- Validate evidence with SHA-256
- Document technical decisions
- Explain limitations honestly
- Organize Git commits
- Present work professionally

## Final Reflection

The biggest lesson from Ticket 001 was that a strong investigation is built from several connected activities.

Log review identified the authentication pattern. Session records confirmed access. File metadata confirmed post-login activity. Wazuh provided additional detection. Containment reduced further risk. The custom detector improved future visibility. Documentation connected all of those steps into one clear explanation.

The project also reminded me that unexpected problems are normal. Monitoring can fail, controls can interrupt testing, scripts can produce noisy alerts, and file transfers can break because of small path errors.

The important part is to recognize the problem, preserve what is known, troubleshoot methodically, document the resolution, and improve the process for the next investigation.
