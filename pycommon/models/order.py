from email.policy import default
from enum import Enum

from .base import MoneyField, Money

from tortoise import Model, fields


class UserOrderSide(str, Enum):
    SELL = "SELL"
    BUY = "BUY"


class UserOrderCompleteStatus(str, Enum):
    UNFILLED = "UNFILLED"
    ERROR = "ERROR"
    PLACED = "PLACED"
    CANCELED = "CANCELED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"


class OrderType(str, Enum):
    LIMIT = "LIMIT"



class UserOrder(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name='user_order')
    currency_pair = fields.ForeignKeyField("models.CurrencyPairs", related_name="order_pairs")
    type = fields.CharEnumField(OrderType)
    amount = MoneyField()
    datetime = fields.DatetimeField(auto_now_add=True)
    price = MoneyField()
    side = fields.CharEnumField(UserOrderSide)
    complete_status = fields.CharEnumField(UserOrderCompleteStatus)    
    commission = MoneyField(default=Money(0))

    def __str__(self) -> str:
        return f"<{self.id} [amount={self.amount}, price={self.price}, side={self.side}, status={self.complete_status}]>"


class CompletedSubOrders(Model):
    id = fields.UUIDField(pk=True)
    user_order = fields.ForeignKeyField("models.UserOrder", related_name="completed_suborders")
    amount = MoneyField()
    price = MoneyField()

    def __str__(self) -> str:
        return f"<{self.id} [amount={self.amount}, price={self.price}]>"
