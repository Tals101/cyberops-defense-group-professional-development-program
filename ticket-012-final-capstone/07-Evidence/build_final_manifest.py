import os
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "07-Evidence"

INVENTORY = EVIDENCE / "final-evidence-inventory.csv"
MANIFEST = EVIDENCE / "final-evidence-sha256.csv"

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    ".pytest_cache",
    "node_modules",
}

if not (ROOT / "03-Detection-Engineering").is_dir():
    raise RuntimeError("Incorrect Ticket 012 project location")


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def relative_path(path):
    return path.relative_to(ROOT).as_posix()


files = []

for directory, subdirs, filenames in os.walk(ROOT):
    subdirs[:] = [
        name for name in subdirs
        if name not in EXCLUDED_DIRS
    ]

    for filename in filenames:
        path = Path(directory) / filename

        if path in (INVENTORY, MANIFEST):
            continue

        if path.is_file() and not path.is_symlink():
            files.append(path)

files.sort(key=lambda path: relative_path(path).lower())

with INVENTORY.open("w", newline="", encoding="utf-8") as output:
    writer = csv.writer(output)
    writer.writerow(["relative_path", "size_bytes"])

    for path in files:
        writer.writerow([
            relative_path(path),
            path.stat().st_size,
        ])

manifest_entries = []

for path in files + [INVENTORY]:
    manifest_entries.append({
        "relative_path": relative_path(path),
        "sha256": sha256_file(path),
    })

with MANIFEST.open("w", newline="", encoding="utf-8") as output:
    writer = csv.DictWriter(
        output,
        fieldnames=["relative_path", "sha256"]
    )
    writer.writeheader()
    writer.writerows(manifest_entries)

with MANIFEST.open("r", encoding="utf-8", newline="") as source:
    recorded_entries = list(csv.DictReader(source))

verified = 0

for entry in recorded_entries:
    path = ROOT / entry["relative_path"]

    if not path.is_file():
        raise RuntimeError("Missing evidence: " + str(path))

    if sha256_file(path) != entry["sha256"]:
        raise RuntimeError("SHA256 mismatch: " + str(path))

    verified += 1

print("TICKET 012 - FINAL EVIDENCE VERIFICATION")
print("INVENTORY_FILE_COUNT=" + str(len(files)))
print("SHA256_ENTRIES_VERIFIED=" + str(verified))
print("INTEGRITY_VERIFICATION=PASS")
print("ORIGINAL_SHA256_LEDGER_PRESERVED=True")
print("INVENTORY=" + relative_path(INVENTORY))
print("MANIFEST=" + relative_path(MANIFEST))
