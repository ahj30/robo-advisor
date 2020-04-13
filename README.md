# Robo-Advisor Project

## Installation
Fork this repository, then clone it to download it locally onto your computer.
Choose a familiar download location like the Desktop.

After cloning the repository, navigate there from the command line:

```sh
cd ~/"Your download location"/robo-advisor
```
## Environment Setup and Security Setup

Create and activate a new Anaconda virtual environment:
```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```
The program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co). But the program's source code should absolutely not include the secret API Key value. Instead, you should set an environment variable called `ALPHAVANTAGE_API_KEY`, and your program should read the API Key from this environment variable at run-time.

Create a ".env" file and place the following inside:

```
ALPHAVANTAGE_API_KEY="your API key"
```

## Usage 
To run the program:

```sh
python app/robo_advisor.py
```

## Example Output
```sh
(stocks-env)
"USER NAME" ~/Desktop/shopping-cart (master)
$ python app/robo_advisor.py
PLEASE ENTER A STOCK SYMBOL: AAPL
-------------------------
SELECTED SYMBOL: AAPL
-------------------------
REQUESTING STOCK MARKET DATA...
REQUEST AT: 2020-02-24 06:39 PM
-------------------------
LATEST DAY: 2020-02-24
LATEST CLOSE: $298.18
52 WEEK HIGH: $327.85
52 WEEK LOW: $170.27
-------------------------
RECOMMENDATION: HOLD
RECCOMENDATION REASON: STOCK IS TRADING WITHIN A CONSOLIDATION RANGE. WAIT TO TAKE ACTION.
-------------------------
WRITING HISTORICAL TRADING DATA TO CSV... C:\Desktop\robo-advisor\data\prices.csv
-------------------------
WOULD YOU LIKE TO SEE A STOCK CHART WITH HISTORICAL PRICES? 'YES' OR 'NO': NO
-------------------------
HAPPY INVESTING!
-------------------------
```

## Testing
Make sure stocks-env is active.
To test:
```sh
pytest
```