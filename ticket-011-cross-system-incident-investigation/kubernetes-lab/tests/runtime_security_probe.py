import json
import os

token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"

status = {}
with open("/proc/self/status", "r", encoding="utf-8") as handle:
    for line in handle:
        if ":" in line:
            key, value = line.split(":", 1)
            status[key] = value.strip()

aws_names = {
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_WEB_IDENTITY_TOKEN_FILE",
    "AWS_ROLE_ARN"
}

result = {
    "classification": "ACTUAL_MINIKUBE_LAB",
    "uid": os.getuid(),
    "euid": os.geteuid(),
    "gid": os.getgid(),
    "egid": os.getegid(),
    "serviceaccount_token_present": os.path.exists(token_path),
    "aws_credential_environment_keys": sorted(
        name for name in os.environ if name in aws_names
    ),
    "effective_capabilities_hex": status.get("CapEff"),
    "no_new_privileges": status.get("NoNewPrivs"),
    "seccomp_mode": status.get("Seccomp")
}

print("RUNTIME_SECURITY_RESULT=" + json.dumps(result, sort_keys=True))
