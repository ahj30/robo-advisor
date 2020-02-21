# app/robo_advisor.py

import requests

import json
import csv
import os
import datetime
from dotenv import load_dotenv
#from matplotlib import pyplot as plt


load_dotenv()

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes. 
    Example: to_usd(4000.444444) 
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

now = datetime.datetime.now()


#
#INFO INPUTS
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

symbol = input("PLEASE ENTER A STOCK SYMBOL: ")
symbol = str(symbol.upper())


request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
weekly_request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={API_KEY}"  
response = requests.get(request_url)
weekly_response = requests.get(weekly_request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)
#print(request_url)

# handle response erors:

if "Error Message" in response.text:
    print("SORRY, SYMBOL NOT FOUND. PLEASE RUN THE PROGRAM AGAIN WITH A VALID SYMBOL.")
    exit()


parsed_response = json.loads(response.text)
weekly_parsed_response = json.loads(weekly_response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsdw = weekly_parsed_response["Weekly Time Series"]
tsd = parsed_response["Time Series (Daily)"]
weekly_dates = list(tsdw.keys())

dates = list(tsd.keys())
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]

high_prices = []
low_prices = []
year_highprices = []
year_lowprices = []



for wdate in weekly_dates[0:51]:
    year_high = tsdw[wdate]["2. high"]
    year_low = tsdw[wdate]["3. low"]
    year_highprices.append(float(year_high))
    year_lowprices.append(float(year_low))

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

fiftytwo_high = max(year_highprices)
fiftytwo_low = min(year_lowprices)

recent_high = max(high_prices)
recent_low = min(low_prices)



#latest_close = parsed_response["Time Series (Daily)"]["2020-02-18"]["4. close"]


#
#INFO OUTPUTS
#
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH (100 TRADING DAYS): {to_usd(float(recent_high))}")
print(f"RECENT LOW (100 TRADING DAYS): {to_usd(float(recent_low))}")
print(f"52 WEEK HIGH: {to_usd(float(fiftytwo_high))}")
print(f"52 WEEK LOW: {to_usd(float(fiftytwo_low))}")
print("-------------------------")


###recommendations:
#### if the stocks latest close is within 5% of recent high, sell. If stock is within 5% of recent low, buy.
#### otherwise hold or take no position

### CHECK IF STOCK IS IN A RANGE
if float(latest_close) > .95*float(recent_high): 
    print("RECOMMENDATION: SELL")
    print("RECOMMENDATION REASON: STOCK IS WITHIN 5% OF ITS MOST RECENT HIGH")
elif float(latest_close) < 1.05*float(recent_low):
    print("RECOMMENDATION: BUY")
    print("RECOMMENDATION REASON: STOCK IS WITHIN 5% OF ITS MOST RECENT LOW")
else:
    print("RECOMMENDATION: HOLD")
    print("RECCOMENDATION REASON: STOCK IS TRADING WITHIN A CONSOLIDATION RANGE")
    

print("-------------------------")
print(f"WRITING PAST 100 DAY TRADING DATA TO CSV... {os.path.abspath(csv_file_path)}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


#print("WOULD YOU LIKE TO SEE THE STOCK GRAPH FOR THE PAST 100 TRADING DAYS?")

#while True:
#    chart_choice = input(str("PLEASE ENTER 'YES' OR 'NO': "))
#    chart_choice = chart_choice.upper()
#
#
#    if chart_choice == "YES":
#        print("GENERATING CHART")
#        break
#    elif chart_choice == "NO":
#        print("HAPPY INVESTING!")
#        print("-------------------------")
#        break
#    else:
#        print("INVALID ENTRY")
#
#print("END")
#
#

