# Ticket 002 - Evidence Integrity Verification

Date: 2026-11-22

Branch: `portfolio-cleanup`

## Finding

Three evidence files in the published repository did not match their SHA-256 values in `evidence/evidence-sha256.txt`.

The files contain HTTP responses with Windows line endings (CRLF) in the headers. When they were first committed, the repository rule `*.txt text eol=lf` converted those line endings to LF. The copies stored by Git therefore differed from the collected files by 7 bytes each.

The local working copies had not been converted and still matched the manifest.

## Correction

1. Added this rule to the root `.gitattributes` so Git stores Ticket 002 evidence byte for byte:

       ticket-002-production-web-application-outage/evidence/** -text

   `evidence/timeline/technical-timeline.md` is documentation, not hashed evidence, and keeps its existing `text eol=lf` setting.

2. Re-staged the evidence folder with `git add --renormalize`. Only the three affected files changed.

3. The manifest `evidence/evidence-sha256.txt` was **not** modified.

## Verification

SHA-256 of the bytes stored by Git, compared with the original manifest:

| File | Previously stored by Git (LF) | Now stored by Git | Manifest | Match |
|---|---|---|---|---|
| `logs/05-baseline-http-response.txt` | `55edc8c0641edc1d06088cc2bd553c7b14b05c319d002a87cc31fb2b428376c4` (552 bytes) | `318dfe4046077f39b44ca4019508dd6b9387c3096eb2f8d8634ba55709fa2f02` (559 bytes) | `318dfe4046077f39b44ca4019508dd6b9387c3096eb2f8d8634ba55709fa2f02` | Yes |
| `logs/09-backend-still-operational.txt` | `87f255ccc832a7b22f512ceef13a87f0e0da914c634cbd736aa223dccb01544f` (554 bytes) | `5ecdc597782b3d92c500c03cde9aaaafea6e617734206750bdc386b5a0126963` (561 bytes) | `5ecdc597782b3d92c500c03cde9aaaafea6e617734206750bdc386b5a0126963` | Yes |
| `logs/19-restored-http-response.txt` | `7a688b7788e3da8557fc39aa565812a9af755acf67f4cda0fddc70af1498a796` (552 bytes) | `362a7c99bb203fcfeec0964110e18b23837acf4b1f88fda1cad495a161d1c306` (559 bytes) | `362a7c99bb203fcfeec0964110e18b23837acf4b1f88fda1cad495a161d1c306` | Yes |

All 23 entries in `evidence/evidence-sha256.txt` match the bytes stored by Git (23 match, 0 mismatch).

To check a file yourself from the repository root:

    git show HEAD:ticket-002-production-web-application-outage/evidence/logs/05-baseline-http-response.txt | sha256sum

The result should equal the value in `evidence/evidence-sha256.txt`.
