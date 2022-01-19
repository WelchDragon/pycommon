from typing import Any, Optional, Type, Union

from .base import Money
from tortoise import Model, fields


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class MoneyField(fields.BigIntField, Money):
    field_type = Money

    @property
    def constraints(self) -> dict:
        return {}

    def to_db_value(self, value: Money, instance: "Union[Type[Model], Model]") -> Optional[int]:
        if isinstance(value, Money):
            return value.val
        return value

    def to_python_value(self, value: Optional[Union[int, float, str, Money]]) -> Optional[Money]:
        if value is None or isinstance(value, Money):
            return value
        return Money(value)
