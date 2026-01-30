import datetime as dt

from pydantic import BaseModel

from .money import Money


class Rebuy(BaseModel):
    amount: Money
    at: dt.datetime


class StackUpdate(BaseModel):
    stack_amount: Money
    at: dt.datetime


class HandNote(BaseModel):
    text: str
    at: dt.datetime
