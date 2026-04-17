from src.domain.interfaces.alert_repository import IAlertrepository
from src.domain.entities.alert import Alert


class MockAlertRepository(IAlertrepository):
    def __init__(self):
        self.alerts = []

    async def add(self, alert: Alert) -> Alert:
        self.alerts.append(alert)
        return alert

    async def get_all(self) -> list[Alert]:
        return self.alerts

    async def get_by_id(self, alert_id):
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert
        return None

    async def delete(self, alert_id):
        self.alerts = [a for a in self.alerts if a.id != alert_id]