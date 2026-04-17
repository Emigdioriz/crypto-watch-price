import pytest
from tests.fixtures.db_fixtures import db_session
from src.infraestructure.repositories.alert_repository_db import AlertrepositoryDB
from src.domain.entities.alert import Alert, AlertStatus
from tests.integration.fixtures.alert_repository_fixtures import alert_in_db, multiple_alerts_in_db


@pytest.mark.asyncio
async def test_add_alert_to_db(db_session):
    repo = AlertrepositoryDB(db_session)
    alert = Alert(symbol="BTCUSD", target_price=50000.00)
    saved_alert = await repo.add(alert)
    assert saved_alert.id is not None
    assert saved_alert.symbol == "BTCUSD"
    assert saved_alert.target_price == 50000.00
    assert saved_alert.status == AlertStatus.PENDING
    assert saved_alert.id == alert.id


@pytest.mark.asyncio
async def test_get_alert_by_id_from_db(db_session, alert_in_db):
    repo = AlertrepositoryDB(db_session)
    found = await repo.get_by_id(alert_in_db.id)
    assert found.id == alert_in_db.id


@pytest.mark.asyncio
async def test_get_all_alerts_from_db(db_session, multiple_alerts_in_db):
    repo = AlertrepositoryDB(db_session)
    found_alerts = await repo.get_all()
    assert len(found_alerts) == len(multiple_alerts_in_db)
    found_ids = {alert.id for alert in found_alerts}
    expected_ids = {alert.id for alert in multiple_alerts_in_db}
    assert found_ids == expected_ids


@pytest.mark.asyncio
async def test_delete_alert_from_db(db_session, alert_in_db):
    repo = AlertrepositoryDB(db_session)
    await repo.delete(alert_in_db.id)
    with pytest.raises(Exception) as exc_info:
        await repo.get_by_id(alert_in_db.id)
    assert "not found" in str(exc_info.value)