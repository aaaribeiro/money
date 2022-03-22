import click
import hashlib
import uuid
from ofxparse import OfxParser

from database import db
from application import schemas
from utils import hash
# import requests
# import click


# URL = "https://api.organizze.com.br/rest/v2/transactions"
# PASSWORD = "ribeirolimand@gmail.com"

# json = {
#     "description": "Computador",
#     "notes": "Pagamento via boleto",
#     "date": "2022-03-21"
# }

# with codecs.open('nubank.ofx') as fileobj:
#     ofx = OfxParser.parse(fileobj)

# account = ofx.account
# print(account.account_id, account.type)

# statement = account.statement
# print(statement.start_date, statement.end_date, statement.balance,)

# for transaction in statement.transactions:
#   print(transaction.date, transaction.amount, transaction.id, transaction.memo, transaction.checknum)


# def getID(string):
#   hash = hashlib.sha256(string.encode("utf-8"))
#   return str(uuid.UUID(hash.hexdigest()[::2]))


def parseData(filename):
  with click.open_file(filename, "rb") as fileobj:
    ofx = OfxParser.parse(fileobj)

  account = ofx.account
  statement = account.statement
  accountID = hash.ID(account.account_id)
  
  # click.secho("Reading elements from ")
  # print(statement.start_date, statement.end_date, statement.balance)
  
  listOfTransactions = []
  for transaction in statement.transactions:
    transactionID = hash.ID(transaction.id)
    transactionObject = schemas.TransactionBase(
      id = transactionID.ID,
      account_id = accountID.ID,
      date = transaction.date,
      amount = transaction.amount,
      memo = transaction.memo
    )
    listOfTransactions.append(transactionObject)
  return listOfTransactions


@click.group()
def main():
  pass


@main.command()
@click.argument("filename", type=click.Path(exists=True))
def importdb(filename):
  transactions = parseData(filename)
  click.secho(f"{len(transactions)} transactions made")
  # print(transactions)


if __name__ == "__main__":
  main()  