# Ticket 001 — SSH Authentication Investigation

<!-- WEEKLY-SUMMARY:START -->

## Ticket Number

**Ticket 001 — SSH Authentication Investigation**

## Objective

Investigate repeated SSH authentication failures against an Ubuntu server, determine whether access succeeded, identify the source and targeted account, preserve supporting evidence, validate Wazuh detections, and apply appropriate containment.

## Environment

| System | Role | Lab IP Address |
|---|---|---|
| Windows 11 | Administration and portfolio storage | 192.168.56.1 |
| Kali Linux | Simulated SSH source | 192.168.56.111 |
| Ubuntu Linux | SSH target and Wazuh agent | 192.168.56.121 |
| Wazuh server | Security monitoring and alert review | 192.168.56.122 |

All activity was performed in an isolated and authorized lab environment.

## Tools Used

- Wazuh manager, dashboard, and Linux agent
- OpenSSH and Windows OpenSSH client
- `sshpass`
- Linux SSH authentication logs
- `journalctl`
- `last` and `lastb`
- Bash
- Cron
- nftables
- Linux account-management commands
- PowerShell
- SHA-256 and `Get-FileHash`
- Microsoft Word and PDF
- SVG
- Git and GitHub

## Investigation Summary

Eleven failed SSH password attempts targeted the `sshlab` account from the Kali Linux system at `192.168.56.111`.

The failures were followed by a successful login from the same source IP. After authentication, the user created `/tmp/ticket001-access.txt`, confirming post-login activity.

The conclusion was supported by:

- Native SSH service logs
- Failed-login records
- Successful-session records
- `last` and `lastb` history
- Post-login file metadata
- Wazuh alerts
- Wazuh screenshots
- Account-lock evidence
- Temporary firewall-rule evidence
- Custom detector output

Wazuh rule 5551 identified repeated failed logins, and rule 40112 identified multiple failures followed by successful authentication.

The affected account was locked, a temporary nftables source-IP block was tested, and a custom Bash detector was scheduled through cron.

## Technical Challenges

### Wazuh monitoring gap

The Wazuh agent was initially pending or disconnected, which created a temporary visibility gap.

Native Ubuntu authentication logs were used as an independent evidence source, and controlled activity was repeated after agent connectivity was confirmed.

### Duplicate detector alerts

The custom detector searched a rolling five-minute window and could alert repeatedly on the same events.

A production version should maintain event state or implement duplicate-alert suppression.

### Temporary firewall interference

The nftables rule successfully blocked SSH traffic but also prevented additional authorized testing.

The temporary rule was removed before testing continued.

### Windows file-transfer error

The first `scp` transfer failed because the Windows destination ended with a trailing backslash.

The problem was resolved by changing into the destination directory and using `.` as the transfer destination.

## Lessons Learned

- Confirm monitoring-agent connectivity before generating activity.
- Verify that logs are reaching the SIEM before testing.
- Use native operating-system logs as an independent source of evidence.
- Define expected results before applying containment controls.
- Record commands and findings while the investigation is underway.
- Add persistent state and duplicate suppression to custom detectors.
- Test transfer paths before the final handoff.
- Automate evidence inventory, hashing, packaging, and validation.
- Clearly separate authorized lab procedures from production recommendations.

<!-- WEEKLY-SUMMARY:END -->


## Overview

This project documents the investigation of repeated SSH authentication failures followed by a successful login to an Ubuntu server.

The investigation identified:

- Eleven failed SSH authentication attempts
- A successful login after the failures
- The source system and targeted account
- Post-login activity
- Relevant Wazuh alerts
- Containment actions
- A custom SSH brute-force detector
- Detection and monitoring limitations

This lab must only be reproduced in an isolated and authorized environment.

## Systems Used

| System | Purpose | IP Address |
|---|---|---|
| Windows host | Administration and evidence storage | 192.168.56.1 |
| Kali Linux | Simulated attacking system | 192.168.56.111 |
| Ubuntu | SSH target and Wazuh agent | 192.168.56.121 |
| Wazuh server | SIEM manager and dashboard | 192.168.56.122 |

Test account:

```text
sshlab
```

Wazuh agent:

```text
ubuntu-lab7
```

## Project Structure

```text
ticket-001-ssh-investigation/
├── README.md
├── detection/
│   ├── detect-ssh-bruteforce.sh
│   └── root-crontab.txt
├── evidence/
│   ├── automatic-detection-alerts.txt
│   ├── complete-ssh-incident-log.txt
│   ├── containment-account-lock.txt
│   ├── containment-firewall-rule.txt
│   ├── cron-detector-execution.txt
│   ├── custom-detection-alert.txt
│   ├── evidence-hashes.txt
│   ├── evidence-inventory.txt
│   ├── failed-attempts-by-ip.txt
│   ├── failed-logins.txt
│   ├── lab-start-time.txt
│   ├── lastb-failures.txt
│   ├── last-successful-login.txt
│   ├── post-login-artifact.txt
│   ├── successful-login-session.txt
│   ├── wazuh-agent-state.txt
│   ├── wazuh-alert-findings.txt
│   ├── wazuh-detection-test-start.txt
│   └── wazuh-test-failed-logins.txt
├── reports/
│   ├── engineering-log.md
│   ├── investigation-report.md
│   └── timeline.csv
└── screenshots/
    ├── wazuh-failures-followed-by-success.png
    └── wazuh-ssh-bruteforce-alert.png
```

## Prerequisites

Another engineer will need:

- An Ubuntu server with SSH enabled
- A Kali Linux system
- A Wazuh manager and dashboard
- A connected Wazuh agent on Ubuntu
- Administrative access to Ubuntu
- Network connectivity between all lab systems
- An isolated lab network
- PowerShell and OpenSSH on Windows

## Reproduction Procedure

### 1. Create the project folders

On Ubuntu:

```bash
mkdir -p ~/ticket-001-ssh-investigation/{evidence,detection,reports,screenshots}
cd ~/ticket-001-ssh-investigation
date -u +"%Y-%m-%dT%H:%M:%SZ" > evidence/lab-start-time.txt
```

### 2. Confirm SSH is running

```bash
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager
sudo ss -lntp | grep ':22'
```

Expected result:

- SSH is active.
- TCP port 22 is listening.

### 3. Create the test account

```bash
sudo useradd -m -s /bin/bash sshlab
sudo passwd sshlab
id sshlab
sudo passwd -S sshlab
```

The account should not have sudo privileges.

Use a temporary password created only for this lab.

### 4. Generate failed authentication attempts

On Kali Linux, install `sshpass` if necessary:

```bash
sudo apt update
sudo apt install -y sshpass
```

Generate eleven failed attempts:

```bash
for attempt in $(seq 1 11); do
    sshpass -p 'INTENTIONALLY_WRONG_TEST_PASSWORD' \
    ssh \
    -o StrictHostKeyChecking=no \
    -o PubkeyAuthentication=no \
    -o PreferredAuthentications=password \
    sshlab@192.168.56.121 \
    'exit'
done
```

Authentication failures are expected.

### 5. Perform a successful login

From Kali:

```bash
ssh sshlab@192.168.56.121
```

After logging in with the correct temporary password:

```bash
whoami
id
date -u
echo "Ticket 001 simulated attacker activity" > /tmp/ticket001-access.txt
ls -l /tmp/ticket001-access.txt
cat /tmp/ticket001-access.txt
exit
```

Expected result:

- The account authenticates successfully.
- The file `/tmp/ticket001-access.txt` is created by `sshlab`.

### 6. Collect SSH evidence

On Ubuntu:

```bash
cd ~/ticket-001-ssh-investigation
```

Collect the complete SSH log:

```bash
sudo journalctl -u ssh --since "30 minutes ago" --no-pager \
> evidence/complete-ssh-incident-log.txt
```

Collect failed login events:

```bash
sudo journalctl -u ssh --since "30 minutes ago" --no-pager |
grep -E "Failed password|authentication failure" \
> evidence/failed-logins.txt
```

Count failures by IP:

```bash
grep "Failed password" evidence/failed-logins.txt |
awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' |
sort |
uniq -c |
sort -nr \
> evidence/failed-attempts-by-ip.txt
```

Collect successful session events:

```bash
sudo journalctl -u ssh --since "30 minutes ago" --no-pager |
grep -E "Accepted password|session opened|session closed" \
> evidence/successful-login-session.txt
```

Collect authentication history:

```bash
sudo lastb -a | head -50 > evidence/lastb-failures.txt
last -ai | head -50 > evidence/last-successful-login.txt
```

Preserve the post-login artifact details:

```bash
{
    sudo stat /tmp/ticket001-access.txt
    echo
    sudo cat /tmp/ticket001-access.txt
} > evidence/post-login-artifact.txt
```

### 7. Review Wazuh detections

Confirm the agent is running:

```bash
sudo systemctl status wazuh-agent --no-pager
sudo tail -50 /var/ossec/logs/ossec.log
```

In the Wazuh dashboard, search for:

```text
agent.name: ubuntu-lab7 AND data.srcip: 192.168.56.111
```

Expected alerts:

#### Wazuh rule 5551

```text
Level: 10
Description: PAM: Multiple failed logins in a small period of time.
MITRE ATT&CK: T1110
```

#### Wazuh rule 40112

```text
Level: 12
Description: Multiple authentication failures followed by a success.
MITRE ATT&CK: T1078 and T1110
```

Save screenshots as:

```text
wazuh-ssh-bruteforce-alert.png
wazuh-failures-followed-by-success.png
```

### 8. Lock the affected account

```bash
sudo passwd -l sshlab
sudo passwd -S sshlab \
> evidence/containment-account-lock.txt
```

The account status should show:

```text
L
```

The account was locked to prevent additional authentication while preserving it for investigation.

### 9. Test a temporary IP block

Create a temporary nftables rule:

```bash
sudo nft add table inet ticket001

sudo nft 'add chain inet ticket001 input { type filter hook input priority 0; policy accept; }'

sudo nft add rule inet ticket001 input \
ip saddr 192.168.56.111 \
tcp dport 22 \
counter drop \
comment '"Ticket001 temporary SSH block"'
```

Save the rule:

```bash
sudo nft list table inet ticket001 \
> evidence/containment-firewall-rule.txt
```

Remove it when testing is complete:

```bash
sudo nft delete table inet ticket001
```

The IP block was temporary because addresses may be shared, reassigned, or spoofed.

### 10. Install the custom detector

The detector is stored at:

```text
detection/detect-ssh-bruteforce.sh
```

Install it:

```bash
sudo cp detection/detect-ssh-bruteforce.sh \
/usr/local/bin/detect-ssh-bruteforce.sh

sudo chmod 750 /usr/local/bin/detect-ssh-bruteforce.sh
```

Run it manually:

```bash
sudo /usr/local/bin/detect-ssh-bruteforce.sh
```

Review detector alerts:

```bash
sudo journalctl -t ssh-bruteforce \
--since "10 minutes ago" \
--no-pager
```

The detector searches five minutes of SSH logs and alerts when at least five failures are found.

### 11. Schedule the detector

Add it to the root crontab:

```bash
(
    sudo crontab -l 2>/dev/null |
    grep -v '/usr/local/bin/detect-ssh-bruteforce.sh'

    echo '* * * * * /usr/local/bin/detect-ssh-bruteforce.sh'
) | sudo crontab -
```

Save the configuration:

```bash
sudo crontab -l > detection/root-crontab.txt
```

Known limitation:

The detector may produce duplicate alerts while the same failures remain inside the five-minute search window.

A production detector should track processed events or suppress duplicate alerts.

## Expected Findings

A successful reproduction should demonstrate:

1. Eleven failed logins originated from `192.168.56.111`.
2. The failures targeted the `sshlab` account.
3. A successful login followed the failures.
4. The successful user created `/tmp/ticket001-access.txt`.
5. Wazuh detected the brute-force activity.
6. Wazuh detected failures followed by a successful login.
7. The affected account was locked.
8. A temporary source-IP block was tested.
9. The custom detector generated an alert.
10. The evidence supported the final investigation conclusion.

## Significant Technical Decisions

### Account lock

The account was locked because it immediately prevented additional password authentication while preserving the account for investigation.

### Temporary IP block

The source IP was temporarily blocked to test network containment. It was not treated as a permanent solution because IP addresses can be shared or reassigned.

### Five-failure threshold

Five failures in five minutes were used to identify concentrated authentication activity while reducing alerts caused by one or two accidental password errors.

### Cron execution

Cron was used because it provided a lightweight method for automatic detector execution without requiring an additional service.

### Evidence hashing

SHA-256 hashes were created to demonstrate that evidence files had not changed after collection.

## Engineering Log

The engineering log is located at:

```text
reports/engineering-log.md
```

It records:

- Date
- Time spent
- What was tried
- What worked
- What failed
- Next step

Two hours were recorded for each workday.

## Evidence Verification

The evidence inventory is located at:

```text
evidence/evidence-inventory.txt
```

The SHA-256 hashes are located at:

```text
evidence/evidence-hashes.txt
```

Each listed file should be recalculated and compared with its recorded hash before submission.

## Windows Transfer

From Windows PowerShell:

```powershell
New-Item `
  -ItemType Directory `
  -Path "$HOME\Desktop\Ticket-001-Transfer" `
  -Force

Set-Location "$HOME\Desktop\Ticket-001-Transfer"

scp -r `
  analyst@192.168.56.121:/home/analyst/ticket-001-ssh-investigation `
  .
```

## Final ZIP Creation

From Windows PowerShell:

```powershell
Compress-Archive `
  -Path ".\ticket-001-ssh-investigation" `
  -DestinationPath ".\Ticket-001-SSH-Investigation.zip" `
  -Force
```

Verify the ZIP:

```powershell
Expand-Archive `
  -Path ".\Ticket-001-SSH-Investigation.zip" `
  -DestinationPath ".\zip-verification" `
  -Force
```

Generate the ZIP checksum:

```powershell
Get-FileHash `
  ".\Ticket-001-SSH-Investigation.zip" `
  -Algorithm SHA256
```

## Cleanup

Only perform cleanup after all evidence has been preserved.

Remove the cron entry:

```bash
(
    sudo crontab -l 2>/dev/null |
    grep -v '/usr/local/bin/detect-ssh-bruteforce.sh'
) | sudo crontab -
```

Remove the installed detector:

```bash
sudo rm -f /usr/local/bin/detect-ssh-bruteforce.sh
```

Remove the temporary firewall table:

```bash
sudo nft delete table inet ticket001
```

Remove the test artifact:

```bash
sudo rm -f /tmp/ticket001-access.txt
```

Remove the test account when it is no longer needed:

```bash
sudo userdel -r sshlab
```
