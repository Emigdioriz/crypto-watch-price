import pytest
from tests.fixtures.db_fixtures import client
from tests.E2E.fixtures.alert_E2E_fixtures import alert_in_db

def test_delete_alert_route(client, alert_in_db):
    response = client.delete(f"/alerts/{alert_in_db.id}")
    assert response.status_code == 204
