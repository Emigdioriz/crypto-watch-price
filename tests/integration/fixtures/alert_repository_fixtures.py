import pytest
from src.domain.entities.alert import Alert

@pytest.fixture
async def alert_in_db(db_session):
    alert = Alert(symbol="BTCUSD", target_price=50000.00)
    db_session.add(alert)
    await db_session.commit()
    await db_session.refresh(alert)
    return alert

@pytest.fixture
async def multiple_alerts_in_db(db_session):
    alerts = [
        Alert(symbol="BTCUSD", target_price=50000.00),
        Alert(symbol="ETHUSD", target_price=4000.00),
        Alert(symbol="XRPUSD", target_price=1.00)
    ]
    db_session.add_all(alerts)
    await db_session.commit()
    for alert in alerts:
        await db_session.refresh(alert)
    return alerts