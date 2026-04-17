import pytest
from tests.factories.alert.alert_factory import AlertFactory
from uuid import UUID


class AlertResponse:
    """Classe auxiliar para representar um alerta criado via API"""
    def __init__(self, id: str):
        self.id = UUID(id)


@pytest.fixture
def alert_in_db(client):
    """Cria um alerta via API usando o client"""
    alert = AlertFactory()
    payload = {
        "symbol": alert.symbol,
        "targetPrice": float(alert.target_price)
    }
    response = client.post("/alerts/", json=payload)    
    alert_id = response.json()["detail"]["id"]
    return AlertResponse(id=alert_id)


@pytest.fixture
def multiple_alerts_in_db(client):
    """Cria múltiplos alertas via API usando o client"""
    alerts = []
    for _ in range(3):
        alert = AlertFactory()
        payload = {
            "symbol": alert.symbol,
            "targetPrice": float(alert.target_price)
        }
        response = client.post("/alerts/", json=payload)