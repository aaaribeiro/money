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

URL = "https://api.organizze.com.br/rest/v2"
USERNAME = "ribeirolimand@gmail.com"
APIKEY = "eb5fa9f870e9ecee79cd56bc61d701d639a2dee0"

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
      amount = f"{transaction.amount:.2f}".replace(".", ""),
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


# def syncAccounts(ctx, param, value):
#   url = f"{URL}/accounts"
#   request = requests.get(url, auth=(USERNAME, APIKEY))
#   print(request.json())
#   ctx.exit()



@main.command()
# @click.option("--accounts", is_flag=True, callback=syncAccounts, 
#                 expose_value=False)
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
        "amount_cents": transaction.amount,
        "notes": transaction.id,
  }
      request = requests.post(url, auth=(username, apiKey), json=payload)


def syncCreditCards(ctx, param, value):

  url = f"{URL}/credit_cards"
  result = requests.get(url, auth=(USERNAME, APIKEY))  

  creditCardList = []
  for creditCard in result.json():
    creditCardList.append(creditCard["name"])
  
  crud = CRUDAccount()
  dbCreditCards = crud.readAccountByType("CREDITCARD")
  for creditCard in dbCreditCards:
    if creditCard.id not in creditCardList:
      click.echo("--> ", nl=None)
      click.secho(creditCard.name.title(), fg="green")
      cardNetwork = click.prompt("Card network")
      dueDate = click.prompt("Due date")
      closingDay = click.prompt("Closing day")
      limit = int(click.prompt("Limit"))
      payload = {
          "name": creditCard.id,
          "card_network": cardNetwork,
          "due_day": dueDate,
          "closing_day": closingDay,
          "limit_cents": limit
      }
      result = requests.post(url, auth=(USERNAME, APIKEY), json=payload)
      if result.status_code == 201:
        click.echo("Credit card ", nl=None)
        click.secho(f"{payload['name']}", fg="blue", nl=None)
        click.echo(" created")
  click.secho("All credit cards synced", fg="green")
  ctx.exit()


def syncAccounts(ctx, param, value):
  
  url = f"{URL}/accounts"
  result = requests.get(url, auth=(USERNAME, APIKEY))  

  accountList = []
  for account in result.json():
    accountList.append(account["name"])

  crud = CRUDAccount()
  dbAccounts = crud.readAccountByType("CC")
  for account in dbAccounts:
    if account.id not in accountList:
      click.echo("--> ", nl=None)
      click.secho(account.name.title(), fg="green")
      payload = {
        "name": account.id,
        "type": "checking",
        "description": account.id,
        "default": False
      }
      result = requests.post(url, auth=(USERNAME, APIKEY), json=payload)
      if result.status_code == 201:
        click.echo("Account ")
        click.secho(f"{payload['name']}", fg="blue")
        click.echo(" created")  
  click.secho("All accounts synced", fg="green")
  ctx.exit()


@main.command()
@click.option("--accounts", is_flag=True, callback=syncAccounts, 
                expose_value=False)
@click.option("--credit-cards", is_flag=True, callback=syncCreditCards, 
                expose_value=False)
def syncdb():
  pass
  # crud = CRUDAccount()
  # text = click.prompt("Category")
  # dbAccounts = crud.readAccountByType(text)
  # for account in dbAccounts:
  #   print(dir(account))



if __name__ == "__main__":
  main()  