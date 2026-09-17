from backend.detector import detect_logs

def test_normal_download() -> None:
    log = {
        "user": "paige.turner@library.book",
        "downloads": 25,
        "bytes": 500_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 60,
    }

    assert detect_logs(log) == []

def test_mass_download_60_downloads() -> None:
    log = {
        "user": "paige.turner@library.book",
        "downloads": 61,
        "bytes": 500_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 60,
    }

    assert len(detect_logs(log)) == 1

def test_mass_download_600_downloads() -> None:
    log = {
        "user": "paige.turner@library.book",
        "downloads": 300,
        "bytes": 500_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 600,
    }
    
    assert len(detect_logs(log)) == 1

def test_normal_hourly_downloads():
    log = {
        "user": "paige.turner@library.book",
        "downloads": 899,
        "bytes": 500_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 3600,
    }

    assert detect_logs(log) == []

def test_mass_download_900_downloads():
    log = {
        "user": "paige.turner@library.book",
        "downloads": 900,
        "bytes": 500_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 3600,
    }

    assert len(detect_logs(log)) == 1


def test_mass_download_6gb():
    log = {
        "user": "paige.turner@library.book",
        "downloads": 100,
        "bytes": 6_000_000_000,
        "connections": 10,
        "denials": 0,
        "download_window": 3600,
    }

    assert len(detect_logs(log)) == 1

def test_permission_probing():
    log = {
        "user": "paige.turner@library.book",
        "downloads": 0,
        "bytes": 0,
        "connections": 10,
        "denials": 30,
        "distinct_denied_items": 5,
        "download_window": 60,
        "denial_window": 300,
    }

    alerts = detect_logs(log)

    assert len(alerts) == 1
    assert alerts[0]["rule"] == "permission_probing"

def test_self_grant_admin():
    log = {
        "user": "paige.turner@library.book",
        "downloads": 0,
        "bytes": 0,
        "connections": 10,
        "denials": 0,
        "self_grant_admin": True,
        "permission_changes": 0,
        "distinct_permission_items": 0,
        "download_window": 60,
        "denial_window": 300,
        "permission_window": 300,
    }

    alerts = detect_logs(log)

    assert len(alerts) == 1
    assert alerts[0]["rule"] == "permission_escalation"
