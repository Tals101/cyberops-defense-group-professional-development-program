STEP 127 - ISOLATED TEST TRUST FIXTURE

Purpose: Test a validly signed but vulnerable image.
This directory contains copies of the release-gate scripts.
Only this fixture trusts the vulnerable test-signing key.
Original production-intended trust configuration is unchanged.
This trust configuration must never authorize a production release.

Test signing key SHA256: 6a7889a21cad6c9455d347c62cc8c10484ecc112f8c027c88ab680495d9d3bb6
Image: 127.0.0.1:5500/ticket010-vulnerable-step125@sha256:ee721dc86416dfd14bce41c1312674a2621b222f58a42312bb8e4d74f92334d3
