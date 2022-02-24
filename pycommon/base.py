from typing import Any

from pydantic import BaseConfig, BaseModel, root_validator

BaseConfig.arbitrary_types_allowed = True


class Money:
    def __init__(self, val: Any) -> None:
        if isinstance(val, int):
            self.val = val
        elif isinstance(val, float):
            self.val = int(val * 100000000)
        elif isinstance(val, Money):
            self.val = val.val
        else:
            raise ValueError(f'invalid money type conversion {val}')        

    def __float__(self) -> str:
        return round(self.val / 100000000, 8)

    def __str__(self) -> str:
        return str(self.__float__())

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[123456.78912345],
            type='number',
            format='float',
        )

    def __gt__(self, other):
        return self.val > Money(other).val

    def __lt__(self, other):
        return self.val < Money(other).val

    def __ge__(self, other):
        return self.val >= Money(other).val

    def __le__(self, other):
        return self.val <= Money(other).val

    def __eq__(self, other):
        return self.val == Money(other).val

    def __ne__(self, other):
        return self.val != Money(other).val

    def __add__(self, other):
        return Money(self.val + Money(other).val)

    __radd__ = __add__

    def __iadd__(self, other):
        self.val = Money(self.val + Money(other).val).val
        return self

    def __sub__(self, other):
        return Money(self.val - Money(other).val)

    def __rsub__(self, other):
        return Money(Money(other).val - self.val)

    def __isub__(self, other):
        self.val = Money(self.val - Money(other).val).val
        return self

    def __mul__(self, other):
        return Money(int(self.val * Money(other).val / 100000000))

    __rmul__ = __mul__

    def __imul__(self, other):
        self.val = Money(self.val * Money(other).val * 100000000).val
        return self

    def __truediv__(self, other):        
        return Money(int(self.val / Money(other).val * 100000000))

    def __rtruediv__(self, other):
        return Money(int(Money(other).val / self.val * 100000000))

    def __itruediv__(self, other):
        self.val = Money(int(self.val / Money(other).val * 100000000) ).val 
        return self

    __div__ = __truediv__
    __rdiv__ = __rtruediv__
    __idiv__ = __itruediv__


class BaseMoney(BaseModel):
    class Config:
        json_encoders = {
            Money: lambda v: float(v),
        }

    @root_validator(pre=True)
    def check_money_type(cls, values):
        '''
        parse class __fields__ dict and find Money fields

        {
            'amount': ModelField(name='amount', type=Money, required=True)
        }

        then convert this fields from 'str' or 'float' to 10^-8 'int'
        '''

        money_fields = list(
            filter(lambda k: cls.__fields__[k].type_ == Money, cls.__fields__),
        )

        for field in money_fields:            
            checked_value = values.get(field)
            
            if not isinstance(checked_value, Money):
                print(type(checked_value))
                if isinstance(checked_value, float):
                    values[field] = Money(round(checked_value * 100000000))                    
                elif isinstance(checked_value, str):
                    values[field] = Money(round(float(checked_value) * 100000000))                    
                elif isinstance(checked_value, int):
                    print(type(checked_value))
                    values[field] = Money(checked_value)                    
                else:
                    raise ValueError(f"'{field}' value should be 'str', 'int', 'float' or 'Money'")
            
        return values
