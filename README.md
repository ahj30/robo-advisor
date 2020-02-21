# Robo-Advisor Project

## Installation
Fork this repository, then clone it to download it locally onto your computer.
Choose a familiar download location like the Desktop.

After cloning the repository, navigate there from the command line:

```sh
cd ~/"Your download location"/robo-advisor
```
### Environment Setup
Create and activate a new Anaconda virtual environment:
```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```
From within the virtual environment, install the required packages specified in the "requirements.txt" file:

```sh
pip install -r requirements.txt
```

#### Usage 
To run the program:

```sh
python app/robo_advisor.py
```

##### Example Output
(stocks-env)
"USER NAME" ~/Desktop/shopping-cart (master)
$ python app/robo_advisor.py
PLEASE ENTER A STOCK SYMBOL: AAPL
-------------------------
SELECTED SYMBOL: AAPL
-------------------------
REQUESTING STOCK MARKET DATA...
REQUEST AT: 2020-02-20 07:31 PM
-------------------------
LATEST DAY: 2020-02-20
LATEST CLOSE: $320.30
RECENT HIGH (100 TRADING DAYS): $327.85
RECENT LOW (100 TRADING DAYS): $215.13
52 WEEK HIGH: $327.85
52 WEEK LOW: $169.50
-------------------------
RECOMMENDATION: SELL
RECOMMENDATION REASON: STOCK IS WITHIN 5% OF ITS MOST RECENT HIGH
-------------------------
WRITING PAST 100 DAY TRADING DATA TO CSV... C:\Users\Andrew\Desktop\robo-advisor\data\prices.csv
-------------------------
HAPPY INVESTING!
-------------------------
