from app.api.routes_health import health


def test_health() -> None:
    assert health()["data"]["state"] == "alive"
