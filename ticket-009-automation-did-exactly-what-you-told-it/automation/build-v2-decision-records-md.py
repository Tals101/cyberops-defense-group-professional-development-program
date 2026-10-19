import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / "evidence" / "v2-automation-decision-record.csv"
OUTPUT = BASE / "evidence" / "v2-automation-decision-record.md"

with SOURCE.open("r", encoding="utf-8-sig") as f:
    records = list(csv.DictReader(f))

lines = []

lines.append("# Ticket #009 — V2 Automation Decision Record")
lines.append("")
lines.append("## Purpose")
lines.append("")
lines.append(
    "This record allows another engineer or auditor to reconstruct each V2 "
    "identity decision without reading the Python source code."
)
lines.append("")
lines.append(
    "Decision chain: **Identity → Evidence → Decision → Authority → Action → Result**"
)
lines.append("")
lines.append("---")
lines.append("")

for index, r in enumerate(records, start=1):
    lines.append(f"# {index}. {r['identity']}")
    lines.append("")

    lines.append("## Identity")
    lines.append("")
    lines.append(f"- Identity: `{r['identity']}`")
    lines.append(f"- Identity type: `{r['identity_type']}`")
    lines.append(f"- Workforce status: `{r['workforce_status']}`")
    lines.append(f"- Owner: `{r['owner']}`")
    lines.append(f"- Business purpose: `{r['business_purpose']}`")
    lines.append(f"- Enabled before evaluation: `{r['enabled_before']}`")
    lines.append("")

    lines.append("## Evidence Considered")
    lines.append("")
    lines.append(
        f"- Days since interactive login: "
        f"`{r['days_since_interactive_login']}`"
    )
    lines.append(
        f"- Days since non-interactive authentication: "
        f"`{r['days_since_noninteractive_auth']}`"
    )
    lines.append(f"- Privilege: `{r['privilege']}`")
    lines.append(f"- Service dependencies: `{r['service_dependencies']}`")
    lines.append(f"- Approval status: `{r['approval_status']}`")
    lines.append(f"- Lifecycle state: `{r['lifecycle_state']}`")
    lines.append(f"- Data freshness: `{r['data_freshness']}`")
    lines.append(
        f"- Evidence completeness: `{r['evidence_completeness']}`"
    )
    lines.append("")

    lines.append("## Decision")
    lines.append("")
    lines.append(f"- Confidence: `{r['confidence']}`")
    lines.append(f"- Decision: `{r['decision']}`")
    lines.append(f"- Reason: {r['decision_reason']}")
    lines.append("")

    lines.append("## Authority")
    lines.append("")
    lines.append(f"- Authority classification: `{r['authority']}`")
    lines.append(f"- Approval required: `{r['approval_required']}`")
    lines.append("")

    lines.append("## Proposed and Actual Action")
    lines.append("")
    lines.append(f"- Proposed action: `{r['proposed_action']}`")
    lines.append(f"- Actual action: `{r['actual_action']}`")
    lines.append(f"- Result: `{r['result']}`")
    lines.append("")

    lines.append("## Recovery")
    lines.append("")
    lines.append(f"- Reversible: `{r['reversible']}`")
    lines.append(f"- Recovery method: {r['recovery_method']}")
    lines.append("")

    lines.append("## Evidence Sources")
    lines.append("")
    lines.append(r["evidence_sources"])
    lines.append("")
    lines.append("---")
    lines.append("")

lines.append("# Auditor Review")
lines.append("")
lines.append(
    "## Could an auditor understand why an account changed without reading "
    "the Python source code?"
)
lines.append("")
lines.append("**Yes.**")
lines.append("")
lines.append(
    "For every evaluated identity, the record contains the identity context, "
    "evidence considered, confidence, decision rationale, authority boundary, "
    "proposed action, actual action, result, and recovery method."
)
lines.append("")
lines.append(
    "The decision record therefore provides an evidence trail independent of "
    "the implementation source code."
)
lines.append("")
lines.append(
    "The CSV version is retained for structured analysis, while this Markdown "
    "version provides human-readable audit evidence."
)

OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Human-readable decision records created: {len(records)}")
print(f"Output: {OUTPUT}")
