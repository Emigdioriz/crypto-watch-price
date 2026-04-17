import pytest
from src.domain.entities.alert import Alert, AlertStatus
from src.application.dtos.alert_dtos import AlertCreateDTO
from tests.unit_test.mocks.mock_alert_repository import MockAlertRepository
from src.application.use_cases.alert_use_cases import CreateAlertUseCase, GetAlertsUseCase, GetAlertByIdUseCase, DeleteAlertUseCase


@pytest.mark.asyncio
async def test_create_alert_use_case():
    # Arrange
    mock_repo = MockAlertRepository()
    use_case = CreateAlertUseCase(repository=mock_repo)
    dto = AlertCreateDTO(symbol="BTCUSDT", targetPrice=50000.00)
    created_alert = await use_case.execute(dto)
    assert created_alert.symbol == dto.symbol
    assert created_alert.target_price == dto.target_price
    assert created_alert.status == AlertStatus.PENDING


@pytest.mark.asyncio
async def test_get_alerts_use_case():
    mock_repo = MockAlertRepository()
    alert1 = await mock_repo.add(Alert(symbol="BTCUSDT", target_price=50000.00))
    alert2 = await mock_repo.add(Alert(symbol="ETHUSDT", target_price=3000.00))
    use_case = GetAlertsUseCase(repository=mock_repo)
    alerts = await use_case.execute()
    assert len(alerts) == 2


@pytest.mark.asyncio
async def test_get_alert_by_id_use_case():
    mock_repo = MockAlertRepository()
    alert = await mock_repo.add(Alert(symbol="BTCUSDT", target_price=50000.00))
    use_case = GetAlertByIdUseCase(repository=mock_repo)
    found = await use_case.execute(alert.id)
    assert found.id == alert.id


@pytest.mark.asyncio
async def test_delete_alert_use_case():
    mock_repo = MockAlertRepository()
    alert = await mock_repo.add(Alert(symbol="BTCUSDT", target_price=50000.00))
    use_case = DeleteAlertUseCase(repository=mock_repo)
    await use_case.execute(alert.id)
    assert await mock_repo.get_by_id(alert.id) is None