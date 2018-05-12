import ccxt
import yaml

# This will a Python object of accounts.yml
User_File = {}

# A simple little function that gives us a US dollar string ($100.00)
def mon(num):
	return "$"+str(round(num, 2))

# Load accounts.yml
with open("accounts.yml", 'r') as stream:
	try:
		User_File = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)

# Check if the user wants to use a different exchange. Else, use kraken
exchange_name = User_File.get('exchange', False)
if (exchange_name):
	exchange_name = str(exchange_name)
	print('Using exchange "'+exchange_name+'"')
	exec('exchange = ccxt.'+exchange_name+"()")
else:
	exchange = ccxt.kraken()

# Populate PRICES object with prices from the exchange
PRICES = {}
# Loop through the "tickers" defined in accounts.yml
for ticker in User_File['tickers']:
	ticker = ticker.upper()
	price = PRICES[ticker] = exchange.fetch_ticker(ticker+'/USD').get('close', False)
	print(ticker, '=', mon(price))


print('---')
print('Your Portfolio:')

total = 0.00 # Total US dollar value of user's portfolio
for account in User_File['accounts']:
	for coin in User_File['accounts'][account]:
		price = PRICES[coin.upper()]
		holdings = User_File['accounts'][account][coin]
		total = total + price * holdings
		print('- ', account.capitalize(), "("+coin.upper()+")", '=', mon(price * holdings))
print('TOTAL:', mon(total))
