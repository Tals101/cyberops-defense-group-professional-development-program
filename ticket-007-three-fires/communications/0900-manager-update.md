# 09:00 — Manager Update

My initial order is **B → A → C**. I am starting with HR-LT-44 because Word launched encoded PowerShell, EDR blocked a child process, and the workstation is still online. I have asked the SOC analyst to identify the source of the APP-PROD-02 `sysadmin` login and establish whether that access was expected. Operations is handling the portal's error spike in parallel: they will preserve logs, compare it with the configuration change, and prepare rollback.

I have not confirmed compromise in any of the three issues. I will change priorities promptly if we see ongoing malicious execution, unauthorized privileged activity, or evidence of successful portal exploitation. The immediate unknowns are what PowerShell actually did and who authorized the SSH session.
