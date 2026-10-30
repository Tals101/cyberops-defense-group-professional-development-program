# Ticket #010 - V3 Evidence Index

## Scope

This index maps the primary V3 security assessment and release-gate evidence to the SHA-256 inventory.

All 24 inventoried files were independently rehashed and checked against their recorded sizes before closure documentation was generated.

## Primary Evidence

| Relative file path | SHA-256 |
|---|---|
| pipeline/v3-release-gate.ps1 | 3DB75FA607C3DD485FCAB258674BE5117B7FFA453064224424F7242BB104BADD |
| pipeline/v3-image-signature-gate.ps1 | A38CD7F543987E96B52203D18E8E294B00FF90997EE584D38BAA64C2FCB689D7 |
| pipeline/v3-vulnerability-gate.ps1 | 7C3708E878A066716C2581C7DD7A2F37B9B5902F59F46D569189622D779BBD93 |
| pipeline/v3-trivy-db-freshness.ps1 | DDB0C9E3B1A9497A4BC1ABF78B971C823475BD14D2E98C187B16E985E933EB54 |
| evidence/v3-final-release-regression.csv | D30F53E4F68782884092E42C3B370AFAECAAA33D5702BB8E145F66FEAA70BD90 |
| evidence/v3-final-release-regression.txt | 0E3B4CEAFDCAE2A806B6EE30168976BE013C01AD4D010A88361FB02201434F1F |
| evidence/v3-signed-vulnerable-release-test.txt | FE81DCC641852BF6C9FA194FC7D805481E825A8E3A5D1476FA20EFE4638FE1D8 |
| evidence/v3-gate-combined-regression-clean.json | 5361DFA7963C7A9ABE2C55159DC3304384DA8288522DB7BCC33EEB50BE811C7C |
| tests/v3-step127-isolated-trust/evidence/v3-gate-combined-regression-vulnerable.json | 8EBA6FD9484C8D8E206092FCBCF6ADFCE8879DA99F556E79D8444EB6E9A2266C |
| investigation/v3-engineering-assessment.md | 47B5EB3A67B80940FCA52DF2116CE7D33DE97A6B657CA14BBB0A25A0515E435A |

## Complete Inventory

File: evidence/v3-evidence-inventory.csv

Inventory SHA-256: D03775C29C10D1DBFB2AC00CF2D565DF6142206E4A8F55E12AE00B41E5A8D7A0

Inventory entry count: 24

## Regression Evidence

- Four expected outcomes were validated.
- The clean signed Alpine candidate passed.
- An unsigned image was rejected.
- An unauthorized signer was rejected.
- A signed vulnerable image was blocked under isolated test trust.
- Original pipeline scripts remained unchanged during the final regression.

## Evidence Interpretation

These records support successful laboratory release-control validation.

They do not independently demonstrate production release authorization, production deployment, or production runtime safety.

## Closure Documentation

- closure/v3-ticket-closure-report.md
- closure/v3-lessons-learned.md
- closure/v3-evidence-index.md

Document integrity hashes are stored in closure/v3-closure-file-hashes.csv.
