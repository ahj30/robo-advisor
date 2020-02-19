# app/robo_advisor.py

import requests
import json
import os
import datetime
from dotenv import load_dotenv

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
response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)
#print(request_url)

# handle response erors:

if "Error Message" in response.text:
    print("SORRY, SYMBOL NOT FOUND. PLEASE RUN THE PROGRAM AGAIN WITH A VALID SYMBOL.")
    exit()


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())
latest_day = dates[0]
latest_close = tsd[latest_day]["4. close"]




#latest_close = parsed_response["Time Series (Daily)"]["2020-02-18"]["4. close"]



#
#INFO OUTPUTS
#

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: " + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print("LATEST DAY: " + last_refreshed)
#print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")