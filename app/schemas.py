# from typing import Optional
from datetime import date
from pydantic import BaseModel

class AccountBase(BaseModel):
    id: str
    name: str
    type: int

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    id: str
    account_id: str
    checknum: str
    type: int
    date: date
    amount: float
    memo: str

    class Config:
        orm_mode = True