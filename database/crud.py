from sqlalchemy.orm import Session

from database import models
from application import schemas


class CrudAccount:

    def createAccount(self, db: Session, payload: schemas.AccountBase):
        dbAccount = models.Accounts(
            id = payload.id,
            name = payload.name,
            type = payload.type
        )
        db.add(dbAccount)
        db.commit()