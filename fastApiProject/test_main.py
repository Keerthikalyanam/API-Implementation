from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_articles():
    response = client.get("/readAlerts", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "service_id": "556",
        "service_name": "my service",
        "alerts": [
            {
                "alert_id": "223",
                "model": "latest model",
                "alert_type": "SMS",
                "alert_ts": "20/10/1972",
                "severity": "High",
                "team_slack": "TRUE"
            }
        ]
    }


def test_create_alert():
    response = client.post(
        "/alerts/",
        headers={"X-Token": "coneofsilence"},
        json={
            "alert_id": "223",
            "service_id": "556",
            "service_name": "my service",
            "model": "latest model",
            "alert_type": "SMS",
            "alert_ts": "20/10/1972",
            "severity": "High",
            "team_slack": "TRUE"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "service_id": "556",
        "service_name": "my service",
        "alerts": [
            {
                "alert_id": "223",
                "model": "latest model",
                "alert_type": "SMS",
                "alert_ts": "20/10/1972",
                "severity": "High",
                "team_slack": "TRUE"
            }
        ]
    }
