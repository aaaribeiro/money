import click
import requests
from ofxparse import OfxParser

from database.crud import (
  CRUDAccount,
  CRUDTransaction,
  CRUDType,
)
from application import schemas
from utils import hash

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

def parseData(filename):
  with click.open_file(filename, "rb") as fileobj:
    ofx = OfxParser.parse(fileobj)

  account = ofx.account
  statement = account.statement
  accountID = hash.ID(account.account_id)

  listOfTransactions = []
  for transaction in statement.transactions:
    transactionID = hash.ID(transaction.id)
    transactionObject = schemas.TransactionBase(
      id = transactionID.ID,
      account_id = accountID.ID,
      date = transaction.date,
      amount = transaction.amount,
      memo = transaction.memo,
    )
    listOfTransactions.append(transactionObject)  
  return schemas.Document(
    start_date = statement.start_date,
    end_date = statement.end_date,
    account_id = accountID.ID,
    transactions = listOfTransactions
  )


@click.group()
def main():
  pass


@main.command()
@click.argument("filename", type=click.Path(exists=True))
def importdb(filename):
  document = parseData(filename)
  click.echo(f"Reading transactions from {document.account_id} between {document.start_date} and {document.end_date}")
  accountID = document.account_id
  crud = CRUDAccount()
  dbAccount =  crud.readAccountByID(accountID)

  if not dbAccount:
    accountName = click.prompt("Account name")
    accountType = click.prompt("Account Type")
    typeID = hash.ID(accountType.lower())
    crud = CRUDType()
    dbType = crud.readTypeByID(typeID.ID)
    
    if not dbType:
      payload = schemas.TypeBase(
        id = typeID.ID,
        name = accountType
      )
      dbType = crud.createType(payload)
     
    payload = schemas.AccountBase(
      id = accountID,
      name = accountName,
      type_id = typeID.ID
    )
    crud = CRUDAccount()
    dbAccount = crud.createAccount(payload)

  transactions = document.transactions
  with click.progressbar(transactions,
                       label="Importing transactions into db",
                       length=len(transactions)) as bar:
    for transaction in bar:
      crud = CRUDTransaction()
      dbTransaction = crud.readTransactionByID(transaction.id)
      if not dbTransaction:
        crud.createTransaction(transaction)
  click.echo("Completed")



@main.command()
def syncdb():
  crud = CRUDTransaction
  transactions = crud.readTransactions()
  url = "https://api.organizze.com.br/rest/v2/transactions"
  username = "ribeirolimand@gmail.com"
  apiKey = "eb5fa9f870e9ecee79cd56bc61d701d639a2dee0"
  with click.progressbar(transactions,
                       label="Syncing transactions in cloud",
                       length=len(transactions)) as bar:
    for transaction in bar:
      payload = {
        "description": transaction.memo,
        "date": str(transaction.date),
        "paid": False,
        "amount_cents": 20050,
        "notes": transaction.id,
  }
      request = requests.post(url, auth=(username, apiKey), json=payload)




if __name__ == "__main__":
  main()  