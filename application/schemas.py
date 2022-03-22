from typing import List
from datetime import date
from pydantic import BaseModel, validator

class AccountBase(BaseModel):
    id: str
    name: str
    type: int

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    id: str
    account_id: str
    # category_id: str
    # checknum: str
    # type: int
    date: date
    amount: float
    memo: str

    @validator("amount")
    def money(cls, value):
        return f"{value:.2f}"

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    id: str
    name: str


class Document(BaseModel):
    account: AccountBase
    transactions: List[TransactionBase]