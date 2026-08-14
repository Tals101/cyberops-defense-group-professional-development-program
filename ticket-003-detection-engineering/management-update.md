Our review confirmed a real monitoring gap. Failed SSH logins were visible, but they were not being tied together by user, source, and time window, so it was difficult to tell a routine password problem from activity that deserved investigation.

I built a detector for five failed SSH passwords against the same account from the same source within two minutes. The first version caught the suspicious test, but it also alerted when a legitimate user repeatedly entered the wrong password and then logged in successfully.

I tuned the second version to consider whether the source is already expected for the account and whether a successful login follows. The updated detector still catches the Kali test while suppressing the legitimate false-positive scenario. Remaining limitations and production recommendations are documented in the final report.
