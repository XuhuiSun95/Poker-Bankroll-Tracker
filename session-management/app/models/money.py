from pydantic import BaseModel, PositiveInt
from pydantic_extra_types.currency_code import ISO4217


class Money(BaseModel):
    amount_cents: PositiveInt
    currency: ISO4217
