from enum import Enum

from pycommon.models.base import BaseModel, MoneyField
from tortoise import Model, fields


class WithdrawalRequestStatus(str, Enum):
    """
    CREATED - initial status
    CONFIRMED - status after user confirmation with email
    SUCCESS - on CONFIRMED webhook
    ERROR - on REMOVED, FAILED, REJECTED webhooks
    PENDING - on SIGNED, UNCONFIRMED, PENDING_APPROVAL webhooks
    """

    INITIAL = "INITIAL"
    CONFIRMED = "CONFIRMED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class DepositRequestStatus(str, Enum):
    """
    CREATED - initial status
    SUCCESS - on CONFIRMED webhook
    ERROR - on REMOVED, FAILED, REJECTED webhooks
    PENDING - on SIGNED, UNCONFIRMED, PENDING_APPROVAL webhooks
    """

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class Balance(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="balance")
    currency = fields.ForeignKeyField("models.Currency")
    amount = MoneyField()

    def __str__(self) -> str:
        return f"<{self.id} [currency_id={self.currency_id}, amount={self.amount}]>"


class HoldBalance(BaseModel):
    order = fields.ForeignKeyField("models.UserOrder", related_name="hold_balance", null=True, blank=True)
    withdrawal = fields.OneToOneField("models.WithdrawalRequest", related_name="hold_balance", null=True, blank=True)
    deposit = fields.OneToOneField("models.DepositRequest", related_name="hold_balance", null=True, blank=True)
    balance = fields.ForeignKeyField("models.Balance", related_name='hold')
    amount = MoneyField()


class WithdrawalRequest(BaseModel):
    tx = fields.CharField(max_length=64, unique=True, default=None)
    user = fields.ForeignKeyField("models.User", related_name="user_withdraw")
    currency = fields.ForeignKeyField("models.Currency")
    status = fields.CharEnumField(WithdrawalRequestStatus, default=WithdrawalRequestStatus.INITIAL)
    amount = MoneyField(default=0)
    datetime = fields.DatetimeField(auto_now_add=True)
    address = fields.CharField(max_length=256)
    fee = MoneyField(default=0)
    net_fee = MoneyField(default=0)

    def __str__(self) -> str:
        return f"<{self.id} [user_id={self.user_id}, currency_id={self.currency_id}]>"


class DepositRequest(Model):
    id = fields.CharField(max_length=32, pk=True)
    tx = fields.CharField(max_length=64, unique=True, default=None)
    user = fields.ForeignKeyField("models.User", related_name="user_deposit")
    currency = fields.ForeignKeyField("models.Currency")
    status = fields.CharEnumField(DepositRequestStatus, default=DepositRequestStatus.PENDING)
    amount = MoneyField(default=0)
    datetime = fields.DatetimeField(auto_now_add=True)
    address = fields.CharField(max_length=256)
    fee = MoneyField(default=0)
    net_fee = MoneyField(default=0)

    def __str__(self) -> str:
        return f"<{self.id} [user_id={self.user_id}, currency_id={self.currency_id}]>"
