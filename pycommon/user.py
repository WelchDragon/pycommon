from pycommon.base_two import BaseModel
from tortoise import fields


class User(BaseModel):
    email = fields.CharField(100, unique=True, index=True)
    password = fields.CharField(128)
    full_name = fields.CharField(130)
    two_fa_token = fields.CharField(130, default='')

    class Meta:
        table = 'db_user'

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
