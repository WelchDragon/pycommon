from .base import BaseModel, MoneyField
from tortoise import fields


class Currency(BaseModel):
    name = fields.CharField(15, unique=True)
    title = fields.CharField(30)
    approval_count = fields.BigIntField()
    network = fields.CharField(100)
    trading_fee_percent = fields.FloatField(default=0)
    trading_min_amount = MoneyField(default = 0)

    def __str__(self) -> str:
        return f"{self.name}"


class CurrencyPairs(BaseModel):
    cur_x = fields.ForeignKeyField("models.Currency", related_name="cur_x")
    cur_y = fields.ForeignKeyField("models.Currency", related_name="cur_y")
    name = fields.CharField(30, unique=True)
    title = fields.CharField(30, default='')

    def __str__(self) -> str:
        return f"<{self.id} [cur_x_id={self.cur_x_id}, cur_y_id={self.cur_y_id}]>"
