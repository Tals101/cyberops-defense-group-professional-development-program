"""
Ticket 012 - Correlation Detector Version 2

Experimental detection improvements.
Preserves the original detector for comparison.
"""

from correlation_detector import (
    APPROVED_DESTINATIONS,
    prepare_event,
    classify_destination,
    classify_identity,
    correlate_deployment_change,
)


def correlate_security_event_v2(network_event, deployment_event=None, window_seconds=300):
    """
    Evaluate destination, identity, workload policy,
    and deployment timing independently.

    Claimed identities are not independently authenticated.
    """

    network = prepare_event(network_event)

    if network["event_type"] != "network_request":
        raise ValueError("Expected network_request event")

    destination_status = classify_destination(network)
    identity_status = classify_identity(network)

    reasons = []
    telemetry_warnings = []

    if deployment_event is None:
        recent_change = False
        telemetry_warnings.append("deployment_telemetry_missing")
    else:
        deployment = prepare_event(deployment_event)

        if deployment["event_type"] == "deployment_change":
            recent_change = correlate_deployment_change(
                network, deployment, window_seconds=window_seconds
            )
        else:
            recent_change = False
            telemetry_warnings.append("deployment_change_not_available")

    if destination_status == "unapproved":
        reasons.append("unapproved_destination")

    if identity_status == "mismatch":
        reasons.append("claimed_identity_mismatch")

    workload = network.get("workload")

    if (
        isinstance(workload, str)
        and workload.strip()
        and workload not in APPROVED_DESTINATIONS
    ):
        reasons.append("workload_not_in_policy")

    if destination_status == "unknown":
        telemetry_warnings.append("destination_classification_unknown")

    if identity_status == "unknown":
        telemetry_warnings.append("identity_telemetry_incomplete")

    alert = bool(reasons)

    if (
        destination_status == "unapproved"
        and identity_status == "mismatch"
        and recent_change
    ):
        triage_level = "high"
    elif destination_status == "unapproved" and recent_change:
        triage_level = "elevated"
    elif alert:
        triage_level = "review"
    else:
        triage_level = "none"

    if recent_change:
        supporting_indicators = ["recent_deployment_change"]
    else:
        supporting_indicators = []

    return {
        "network_event_id": network["event_id"],
        "destination_status": destination_status,
        "identity_status": identity_status,
        "recent_deployment_change": recent_change,
        "alert": alert,
        "triage_level": triage_level,
        "reasons": reasons,
        "supporting_indicators": supporting_indicators,
        "telemetry_warnings": telemetry_warnings,
    }
