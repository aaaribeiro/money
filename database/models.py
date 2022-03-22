from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Float,
    Date,
)
from sqlalchemy.orm import relationship
from database.db import Base


class Accounts(Base):
    __tablename__ = "accounts"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(Integer)
    transactions = relationship("Transactions", back_populates="account")  


class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True)
    account_id = Column(ForeignKey("accounts.id"))
    category_id = Column(ForeignKey("categories.id"))
    checknum = Column(String)
    type = Column(Integer)
    date = Column(Date)
    amount = Column(Float)
    memo = Column(String)
    account = relationship("Accounts", back_populates="transactions")
    category = relationship("Categories", back_populates="transactions")


class Categories(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    transactions = relationship("Transactions", back_populates="category")