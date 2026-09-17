MASS_DOWNLOAD_RULES = [
    {"downloads": 20, "seconds": 60},
    {"downloads": 100, "seconds": 600},
    {"downloads": 300, "seconds": 3600},
    {"bytes": 2_000_000_000, "seconds": 3600},
]

PERMISSION_PROBING_RULES = [
    {"denials": 10, "seconds": 300, "distinct_items": 5},
    {"denials": 30, "seconds": 3600},
]

PERMISSION_ESCALATION_RULES = [
    {"self_grant_admin": True},
    {"permission_changes": 10, "seconds": 300, "distinct_items": 5},
    {"permission_changes": 25, "seconds": 3600},
]

def detect_logs(log) -> list[dict]:
    alerts = []

    for rule in MASS_DOWNLOAD_RULES:

        threshold = rule.get("downloads")

        if threshold is not None:
            if (
                log["downloads"] >= threshold * 3
                and log["download_window"] == rule["seconds"]
            ):
                alerts.append(
                    {
                        "user": log["user"],
                        "rule": "mass_download",
                        "message": (
                            f"Too many downloads detected: "
                            f"{log['downloads']} downloads in "
                            f"{log['download_window']} seconds."
                        ),
                    }
                )

        threshold = rule.get("bytes")

        if threshold is not None:
            if (
                log["bytes"] >= threshold * 3
                and log["download_window"] == rule["seconds"]
            ):
                alerts.append(
                    {
                        "user": log["user"],
                        "rule": "mass_download",
                        "message": (
                            f"Too much data downloaded: "
                            f"{log['bytes']} bytes in "
                            f"{log['download_window']} seconds."
                        ),
                    }
                )
    
    for rule in PERMISSION_PROBING_RULES:
        if (
            log["denials"] >= rule["denials"] * 3
            and log["denial_window"] == rule["seconds"]
            and log["distinct_denied_items"] >= rule.get("distinct_items", 0)
        ):
            alerts.append(
                {
                    "user": log["user"],
                    "rule": "permission_probing",
                    "message": (
                        f"Too many permission denials detected: "
                        f"{log['denials']} denials in "
                        f"{log['denial_window']} seconds."
                    ),
                }
            )

    for rule in PERMISSION_ESCALATION_RULES:

        if rule.get("self_grant_admin"):
            if log.get("self_grant_admin", False):
                alerts.append(
                    {
                        "user": log["user"],
                        "rule": "permission_escalation",
                        "message": (
                            "User granted themselves owner/admin permissions."
                        ),
                    }
                )

        else:
            if (
                log.get("permission_changes", 0) >= rule["permission_changes"] * 3
                and log.get("permission_window", 0) == rule["seconds"]
                and log.get("distinct_permission_items", 0)
                >= rule.get("distinct_items", 0)
            ):
                alerts.append(
                    {
                        "user": log["user"],
                        "rule": "permission_escalation",
                        "message": (
                            f"Too many permission changes detected: "
                            f"{log['permission_changes']} changes in "
                            f"{log['permission_window']} seconds."
                        ),
                    }
                )
 
    return alerts