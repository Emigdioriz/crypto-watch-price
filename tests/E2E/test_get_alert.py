import pytest
from tests.fixtures.db_fixtures import db_session, client
from tests.E2E.fixtures.alert_E2E_fixtures import alert_in_db, multiple_alerts_in_db

def test_get_alerts_route(client, multiple_alerts_in_db):
    response = client.get("/alerts/")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data is not None


def test_get_alert_by_id_route(client, alert_in_db):
    response = client.get(f"/alerts/{alert_in_db.id}")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data
    assert data["detail"]["id"] == str(alert_in_db.id)