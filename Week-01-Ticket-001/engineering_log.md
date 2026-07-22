# Engineering Log

## July 20, 2026

**Time spent:** 2 hours

### What I tried

- Established the SSH investigation lab baseline.
- Generated repeated failed SSH authentication attempts from Kali Linux at 192.168.56.111.
- Targeted the `sshlab` account on the Ubuntu server at 192.168.56.121.
- Performed a successful SSH login after the failed attempts.
- Created `/tmp/ticket001-access.txt` to simulate post-login activity.
- Reviewed SSH service logs, `last`, `lastb`, and Wazuh alerts.
- Tested temporary source-IP blocking with nftables.
- Locked the compromised `sshlab` account.
- Created and scheduled a custom SSH brute-force detection script.

### What worked

- Linux logs identified the failed authentication attempts, source IP, target account, and successful session.
- Wazuh rule 5551 detected multiple failed PAM logins.
- Wazuh rule 40112 detected multiple authentication failures followed by a successful login.
- The post-login file confirmed that authenticated activity occurred.
- The account lock prevented additional use of the `sshlab` account.
- The nftables rule temporarily blocked SSH traffic from the Kali source.
- The custom detector generated alerts when the failure threshold was reached.
- Cron successfully executed the detector automatically.

### What failed

- The Wazuh agent was initially pending or disconnected, creating a temporary monitoring gap.
- The custom detector generated duplicate alerts while the same failed events remained inside its five-minute search window.
- The temporary nftables rule blocked later testing traffic and had to be removed.
- Password-based SSH authentication allowed the simulated credential attack to succeed.

### My next step

- Complete the investigation report and incident timeline.
- Preserve the evidence and calculate SHA-256 hashes.
- Transfer the completed project and screenshots to the Windows host.
- Add documentation that allows another engineer to reproduce the investigation.

---

## July 22, 2026

**Time spent:** 2 hours

### What I tried

- Updated the project evidence inventory.
- Regenerated SHA-256 hashes for the investigation files.
- Transferred the project from Ubuntu to the Windows host.
- Added the two Wazuh screenshots to the transferred project.
- Regenerated the Windows project inventory and hashes.
- Verified every file against its recorded SHA-256 hash.
- Created and tested the final ZIP archive.
- Created a separate SHA-256 checksum file for the ZIP archive.
- Created the complete README reproduction guide.
- Created the Weekly Ticket Closure Package.
- Rebuilt and verified the final 28-file ZIP archive.

### What worked

- The complete project transferred successfully to Windows.
- Both Wazuh screenshots were added to the project.
- All 27 hash-listed project files passed SHA-256 integrity verification; evidence-hashes.txt was intentionally excluded from self-hashing.
- The final ZIP archive extracted successfully and contained all 28 expected files.
- The ZIP checksum matched the recorded SHA-256 value.
- The README documented the complete reproduction procedure.

### What failed

- The first `scp` transfer failed because the Windows destination ended with a trailing backslash that was interpreted incorrectly.
- Changing into the destination directory and using `.` as the destination corrected the transfer problem.
- The screenshots directory was initially empty because the screenshots had remained on the Windows host.

### My next step

- Submit the completed and verified Ticket 001 project.
- Retain the ZIP checksum with the final submission.
