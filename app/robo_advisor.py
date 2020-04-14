# app/robo_advisor.py

import requests
import pandas as pd
import plotly.graph_objects as go

import json
import csv
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
##check for digits in stock symbol
def high_low():
    """
    calculates the highs and lows from the given time series
    """
    for date in dates:
        high_price = tsd[date]["2. high"]
        low_price = tsd[date]["3. low"]
        high_prices.append(float(high_price))
        low_prices.append(float(low_price))    
def display_chart():
    """
    displays chart given the csv data
    """
    df = pd.read_csv(csv_file_path)
    fig = go.Figure(go.Scatter(x = df['timestamp'], y = df['close'],
                    name='Share Prices (in USD)'))
    fig.update_layout(title= symbol + ' Prices over time',
                    plot_bgcolor='rgb(230, 230 ,230)',
                    showlegend=True)
    fig.show()
    print("LOADING CHART...")
    line_seperator()    
def response_errors():
    """ 
    displays error messages given a certain stock symbol
    """
    if "Error Message" in response.text:
        print("SORRY, SYMBOL NOT FOUND. PLEASE RUN THE PROGRAM AGAIN WITH A VALID SYMBOL.")
        exit()
    if  "Thank you for using Alpha Vantage!" in response.text:
        print("TOO MANY REQUESTS. PLEASE WAIT 30 SECONDS AND TRY AGAIN.")
        exit()
def hasNumbers(inputString): 
    """
    Checks if a string has any numbers in it
    Param: inputString (string) checks if it has any numbers
    Example: if inputString = "12tl" then hasNumbers(inputString) == True
    """
    return any(char.isdigit() for char in inputString)
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes. 
    Param: my_price (numeric, like int or float) the number to be formatted.
    Example: to_usd(4000.444444) 
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
def human_friendly_timestamp(current_time):
    """
    Formats the time of checkout to user friendly format.
    Param: current_time, the datetime to be formatted.
    Example: Make 2020-4-1 18:12:13 into 2020-04-01 06:12:13 PM
    """
    return current_time.strftime("%Y-%m-%d %I:%M:%S %p")
def write_csv(dates, csv_file_path):
    """
    Writes time series data to CSV. 
    Params: dates-list of the keys from time series, csv_file_path- where to be written.
    Example: take the time-series stock data for each day and write it to csv file.
    """
    csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
    with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() 
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
    return True
def line_seperator():
    """
    lines to be printed
    """
    print("-------------------------")
def recommendation(close,high,low):
    """
    formulas that calculate the stock recommendation
    Params: close and high and low (all float)- compared to each other to give recommendation.
    Example: If high is within 5% of close, recommendation to sell will be output.
    """
    if float(close) > .95*float(high): 
        print("RECOMMENDATION: SELL")
        print("RECOMMENDATION REASON: STOCK IS WITHIN 5% OF ITS RECENT HIGH")
        return True
    elif float(close) < 1.05*float(low):
        print("RECOMMENDATION: BUY")
        print("RECOMMENDATION REASON: STOCK IS WITHIN 5% OF ITS RECENT LOW")
        return True
    else:
        print("RECOMMENDATION: HOLD")
        print("RECCOMENDATION REASON: STOCK IS TRADING WITHIN A CONSOLIDATION RANGE. IT IS NOT NEAR A RECENT HIGH OR LOW.")
        return False

now = datetime.datetime.now()
time = human_friendly_timestamp(now)

#INFO INPUTS
if __name__ == "__main__":
    while True:
        symbol = input("PLEASE ENTER A STOCK SYMBOL: ")
        if hasNumbers(symbol) == True:
            print("STOCK SYMBOL CANNOT CONTAIN DIGITS")
        else:
            break
        
    API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")
    symbol = str(symbol.upper())
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    response_errors()
    #parse the stock data
    parsed_response = json.loads(response.text)    
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    tsd = parsed_response["Time Series (Daily)"]   
    dates = list(tsd.keys())
    latest_day = dates[0]
    latest_close = tsd[latest_day]["4. close"]
    #calculate highs and lows
    high_prices = []
    low_prices = []   
    high_low()
    recent_high = max(high_prices)
    recent_low = min(low_prices)
    #writing to CSV    
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
    write_csv(dates, csv_file_path)
    #output
    line_seperator()
    print(f"SELECTED SYMBOL: {symbol}")
    line_seperator()
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT: " + time )
    line_seperator()
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH (100 TRADING DAYS): {to_usd(float(recent_high))}")  
    print(f"RECENT LOW (100 TRADING DAYS): {to_usd(float(recent_low))}")
    line_seperator()
    recommendation(latest_close,recent_high,recent_low)
    line_seperator()
    print(f"WRITING HISTORICAL TRADING DATA TO CSV... {os.path.abspath(csv_file_path)}")
    line_seperator()
    #displays chart
    while True:
        chart_choice = input("WOULD YOU LIKE TO SEE A STOCK CHART WITH HISTORICAL PRICES? 'YES' OR 'NO': ")
        chart_choice = chart_choice.upper()
        if chart_choice == "YES":
            display_chart()
            break
        elif chart_choice == "NO":
            line_seperator()
            break
        else:
            print("PLEASE ENTER EITHER 'YES' OR 'NO'" )
    print("HAPPY INVESTING!")
    line_seperator()   
#end