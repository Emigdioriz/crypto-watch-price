import factory
from faker import Faker
from src.domain.entities.alert import Alert, AlertStatus

fake = Faker()

class AlertFactory(factory.Factory):
    class Meta:
        model = Alert

    symbol = factory.LazyAttribute(lambda _: fake.currency_code())
    target_price = factory.LazyAttribute(lambda _: fake.pydecimal(left_digits=5, right_digits=2, positive=True))