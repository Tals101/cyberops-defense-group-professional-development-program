import json
import urllib.error
import urllib.request

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({})
)

tests = [
    (
        "pod_health",
        "http://127.0.0.1:8080/health",
        200,
        {"status": "ok", "environment": "isolated-lab"}
    ),
    (
        "pod_report",
        "http://127.0.0.1:8080/report",
        200,
        {"report_type": "synthetic", "records": 0}
    ),
    (
        "service_health",
        "http://reporting-api.ticket-011-lab.svc:8080/health",
        200,
        {"status": "ok"}
    ),
    (
        "service_report",
        "http://reporting-api.ticket-011-lab.svc:8080/report",
        200,
        {"contains_real_financial_data": False}
    ),
    (
        "service_unknown_route",
        "http://reporting-api.ticket-011-lab.svc:8080/not-found",
        404,
        {"error": "not_found"}
    )
]

results = []

for name, url, expected_status, expected_fields in tests:
    try:
        response = opener.open(url, timeout=8)
    except urllib.error.HTTPError as error:
        response = error

    try:
        status = response.getcode()
        body = json.loads(response.read().decode("utf-8"))
    finally:
        response.close()

    if status != expected_status:
        raise AssertionError(
            f"{name}: expected {expected_status}, got {status}"
        )

    for field, expected in expected_fields.items():
        if body.get(field) != expected:
            raise AssertionError(
                f"{name}: unexpected value for {field}"
            )

    results.append({
        "test": name,
        "status": status,
        "result": "PASS",
        "response": body
    })

print("LIVE_HTTP_RESULT=" + json.dumps({
    "classification": "ACTUAL_MINIKUBE_LAB",
    "tests": results,
    "passed": len(results),
    "failed": 0
}, sort_keys=True))
