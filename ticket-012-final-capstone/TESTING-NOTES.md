# Ticket 012 - Testing Notes

Date: 2026-11-22

These notes add to the test commands in `README.md`. The README is listed in the evidence manifest (`07-Evidence/final-evidence-sha256.csv`), so it is left unchanged and the warning is recorded here.

## Running the tests changes preserved evidence

`03-Detection-Engineering/tests/test_detector_cli.py` writes its report to:

    07-Evidence/supporting-outputs/detector-cli-error-handling-tests.txt

That file is listed in `07-Evidence/final-evidence-sha256.csv`. Running the test in this folder overwrites it, and the file may then no longer match its recorded SHA-256 value (for example, if line endings differ from the original run).

The comparison and adversarial scripts listed in the README (`compare_baselines.py`, `compare_detectors_v2.py` and `run_adversarial_validation.py`) also regenerate files under `07-Evidence/` and `04-Adversarial-Validation/evidence/`.

## Recommended approach

Run the tests and scripts in a disposable copy, not in the preserved evidence directory. For example, from the repository root in PowerShell:

    Copy-Item -Recurse .\ticket-012-final-capstone "$env:TEMP\ticket-012-test-copy"
    Set-Location "$env:TEMP\ticket-012-test-copy"
    python .\03-Detection-Engineering\tests\test_correlation_detector.py
    python .\03-Detection-Engineering\tests\test_correlation_detector_v2.py
    python .\03-Detection-Engineering\tests\test_detector_cli.py

When finished, delete the temporary copy. To check that the preserved evidence is unchanged, compare the files in `07-Evidence/` against `07-Evidence/final-evidence-sha256.csv`.

## Observed result

On November 22, 2026, all three test files passed in a disposable copy: 31 V1, 9 V2 and 11 CLI tests (51 total). The CLI test rewrote its report file in that copy, as described above. The preserved evidence in this repository was not changed.
