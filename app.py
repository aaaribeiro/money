from ofxparse import OfxParser


import codecs
with codecs.open('extrato.ofx') as fileobj:
    ofx = OfxParser.parse(fileobj)

# Account
account = ofx.account
print(account.account_id, account.type)

# Statement

statement = account.statement
print(
statement.start_date,          # The start date of the transactions
statement.end_date,            # The end date of the transactions
statement.balance,             # The money in the account as of the statement date
# statement.available_balance,   # The money available from the account as of the statement date
# statement.transactions,
)        # A list of Transaction objects

# Transaction

for transaction in statement.transactions:
  print(
#   transaction.payee,
#   transaction.type,
  transaction.date,
#   transaction.user_date,
  transaction.amount,
  transaction.id,
  transaction.memo,
#   transaction.sic,
#   transaction.mcc,
  transaction.checknum
  )

# # InvestmentTransaction

# for transaction in statement.transactions:
#   transaction.type
#   transaction.tradeDate
#   transaction.settleDate
#   transaction.memo
#   transaction.security      # A Security object
#   transaction.income_type
#   transaction.units
#   transaction.unit_price
#   transaction.comission
#   transaction.fees
#   transaction.total
#   transaction.tferaction

# # Positions

# for position in statement.positions:
#   position.security       # A Security object
#   position.units
#   position.unit_price
#   position.market_value

# # Security

# security = transaction.security
# # or
# security = position.security
# security.uniqueid
# security.name
# security.ticker
# security.memo

# import requests
# import click


# URL = "https://api.organizze.com.br/rest/v2/transactions"
# PASSWORD = "ribeirolimand@gmail.com"

# json = {
#     "description": "Computador",
#     "notes": "Pagamento via boleto",
#     "date": "2022-03-21"
# }

