from unicodedata import category
from sqlalchemy.orm import Session

from database import models
from database.db import Base, engine
Base.metadata.create_all(engine)

from application import schemas
from utils.handler import DbHandler


class CRUDAccount:

    def readAccountByID(self, id: str):
        with DbHandler() as db:
            dbAccount = db.query(models.Accounts).get(id)
        return dbAccount


    def readAccountByType(self, type: str):
        with DbHandler() as db:
            dbAccounts = db.query(models.Accounts).\
                filter(models.Accounts.type.has(models.Types.name==type)).\
                all()
        return dbAccounts


    def createAccount(self, payload: schemas.AccountBase):
        with DbHandler() as db:
            dbAccount = models.Accounts(
                id = payload.id,
                name = payload.name.upper(),
                type_id = payload.type_id
            )
            db.add(dbAccount)
            db.commit()
            db.refresh(dbAccount)
        return dbAccount


class CRUDType:

    def readTypeByID(self, id: str):
        with DbHandler() as db:
            dbType = db.query(models.Types).get(id)
        return dbType
    

    def createType(self, payload: schemas.TypeBase):
        with DbHandler() as db:
            dbType = models.Types(
                id = payload.id,
                name = payload.name.upper(),
            )
            db.add(dbType)
            db.commit()
            db.refresh(dbType)
        return dbType


class CRUDTransaction:

    def readTransactions():
        with DbHandler() as db:
            dbTransactions = db.query(models.Transactions).all()
        return dbTransactions

    
    def readTransactionByID(self, id: str):
        with DbHandler() as db:
            dbTransaction = db.query(models.Transactions).get(id)
        return dbTransaction

    
    def createTransaction(self, payload: schemas.TransactionBase):
        with DbHandler() as db:
            dbTransaction = models.Transactions(
                id = payload.id,
                account_id = payload.account_id,
                date = payload.date,
                amount = payload.amount,
                memo = payload.memo.upper(),
            )
            db.add(dbTransaction)
            db.commit()
            db.refresh(dbTransaction)
        return dbTransaction
