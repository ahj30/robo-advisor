import os
import pytest
from datetime import datetime
from app.robo_advisor import to_usd, hasNumbers, human_friendly_timestamp, write_csv, recommendation

def test_to_usd():
    # it should apply USD formatting
    assert to_usd(4.50) == "$4.50"

    # it should display two decimal places
    assert to_usd(4.5) == "$4.50"

    # it should round to two places
    assert to_usd(4.55555) == "$4.56"

    # it should display thousands separators
    assert to_usd(1234567890.5555555) == "$1,234,567,890.56"

def test_hasNumbers():
    #check if string has or does not have numbers
    string = "hello"
    assert hasNumbers(string) == False
    
    numbers = "12kj45"
    assert hasNumbers(numbers) == True

def test_human_friendly_timestamp():
    # check for 12 hour scale and PM time
    test_date = datetime(2020, 4, 1, 16, 31, 16)
    assert human_friendly_timestamp(test_date) == "2020-04-01 04:31:16 PM"

    # check for AM time
    testtwo_date =datetime (2020, 12, 27, 3, 18, 22)
    assert human_friendly_timestamp(testtwo_date) == "2020-12-27 03:18:22 AM"



def test_write_csv():

    # SETUP

    example_rows = [
        {"timestamp": "2019-06-08", "open": "101.0924", "high": "101.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-07", "open": "102.6500", "high": "102.6900", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-06", "open": "102.4800", "high": "102.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "102.3300", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-04", "open": "101.2600", "high": "101.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-01", "open": '99.2798',  "high": "100.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
    ]

    csv_filepath = os.path.join(os.path.dirname(__file__), "example_reports", "temp_prices.csv")

    if os.path.isfile(csv_filepath):
        os.remove(csv_filepath)

    assert os.path.isfile(csv_filepath) == False 
    # INVOCATION

    #result = write_csv(example_rows, csv_filepath)

    # EXPECTATIONS

    #assert result == True
    #assert os.path.isfile(csv_filepath) == True   

def test_recommendation():
    close = 100
    high = 110
    low = 90
    assert recommendation(close,high,low) == False
    close = 100
    high = 101
    low = 90
    assert recommendation(close,high,low) == True
    close = 100
    high = 110
    low = 99
    assert recommendation(close,high,low) == True

