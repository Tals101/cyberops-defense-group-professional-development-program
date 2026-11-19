"""
Ticket 012 - Multi-Dimensional Correlation Detector

Purpose:
Correlate workload identity, network destination,
deployment changes, and authorization events.
"""

from datetime import datetime, timezone


def normalize_timestamp(value):
    """
    Convert an ISO 8601 timestamp to UTC.

    Reject missing, malformed, or timezone-naive values.
    """

    if not isinstance(value, str) or not value.strip():
        raise ValueError("Missing or invalid timestamp")

    try:
        timestamp = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except ValueError:
        raise ValueError("Malformed timestamp")

    if timestamp.tzinfo is None:
        raise ValueError("Timestamp must include timezone")

    return timestamp.astimezone(timezone.utc)


def prepare_event(event):
    """
    Validate common security event fields and
    normalize the event timestamp to UTC.
    """

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")

    required_fields = ("event_id", "event_type", "timestamp")

    for field in required_fields:
        if (
            not isinstance(event.get(field), str)
            or not event[field].strip()
        ):
            raise ValueError(f"Missing or invalid {field}")

    normalized = dict(event)

    normalized["timestamp"] = (
        normalize_timestamp(event["timestamp"])
        .isoformat()
        .replace("+00:00", "Z")
    )

    return normalized


def deduplicate_events(events):
    """
    Normalize events, detect duplicate event IDs,
    and identify conflicting duplicate records.
    """

    if not isinstance(events, list):
        raise ValueError("Events must be a list")

    unique_events = []
    duplicates = []
    seen = {}

    for event in events:
        prepared = prepare_event(event)
        event_id = prepared["event_id"]

        if event_id in seen:
            duplicates.append({
                "event_id": event_id,
                "conflict": prepared != seen[event_id]
            })
            continue

        seen[event_id] = prepared
        unique_events.append(prepared)

    return {
        "events": unique_events,
        "duplicates": duplicates
    }


APPROVED_DESTINATIONS = {
    "application-api": {
        "http://internal-service:8080/resource"
    }
}


def classify_destination(event):
    """
    Classify a network destination using the
    approved destination list for its workload.
    """

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")

    workload = event.get("workload")
    destination = event.get("destination")

    if (
        not isinstance(workload, str)
        or not isinstance(destination, str)
        or not workload.strip()
        or not destination.strip()
    ):
        return "unknown"

    approved = APPROVED_DESTINATIONS.get(workload)

    if approved is None:
        return "unknown"

    if destination in approved:
        return "approved"

    return "unapproved"


def correlate_deployment_change(network_event, deployment_event, window_seconds=300):
    """
    Determine whether a network event occurred shortly
    after a deployment change affecting the same workload.
    """

    network = prepare_event(network_event)
    deployment = prepare_event(deployment_event)

    if network["event_type"] != "network_request":
        return False

    if deployment["event_type"] != "deployment_change":
        return False

    if network.get("workload") != deployment.get("workload"):
        return False

    if not network.get("workload"):
        return False

    network_time = normalize_timestamp(network["timestamp"])
    deployment_time = normalize_timestamp(deployment["timestamp"])

    difference = (network_time - deployment_time).total_seconds()

    return 0 <= difference <= window_seconds


def classify_identity(event):
    """
    Compare an observed workload identity with
    the identity claimed by the requesting client.
    """

    if not isinstance(event, dict):
        raise ValueError("Event must be a dictionary")

    workload = event.get("workload")
    claimed_identity = event.get("claimed_identity")

    if (
        not isinstance(workload, str)
        or not isinstance(claimed_identity, str)
        or not workload.strip()
        or not claimed_identity.strip()
    ):
        return "unknown"

    if workload == claimed_identity:
        return "matched"

    return "mismatch"


def correlate_security_event(network_event, deployment_event):
    """
    Correlate destination, deployment timing,
    and workload identity indicators.
    """

    network = prepare_event(network_event)
    deployment = prepare_event(deployment_event)

    if network["event_type"] != "network_request":
        raise ValueError("Expected network_request event")

    destination_status = classify_destination(network)
    identity_status = classify_identity(network)

    recent_change = correlate_deployment_change(
        network, deployment
    )

    alert = (
        destination_status == "unapproved"
        and recent_change
    )

    if alert and identity_status == "mismatch":
        triage_level = "high"
    elif alert:
        triage_level = "review"
    else:
        triage_level = "none"

    return {
        "network_event_id": network["event_id"],
        "deployment_event_id": deployment["event_id"],
        "destination_status": destination_status,
        "identity_status": identity_status,
        "recent_deployment_change": recent_change,
        "alert": alert,
        "triage_level": triage_level
    }
