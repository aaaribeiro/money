from typing import List, Optional
from datetime import date
from pydantic import BaseModel, validator

class AccountBase(BaseModel):
    id: str
    type_id: str
    name: str
    
    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    id: str
    account_id: str
    category_id: Optional[str]
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

    class Config:
        orm_mode = True


class TypeBase(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class Account(BaseModel):
    id: str
    type: str
    name: str
    
    class Config:
        orm_mode = True


class Document(BaseModel):
    start_date: date
    end_date: date
    account_id: str
    transactions: List[TransactionBase]

    class Config:
        orm_mode = True