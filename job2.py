import time
import datetime
import sys
import yfinance as yf
import sqlite3


def jobChecker(value):
    conn = sqlite3.connect('data.db')
    cursor = conn.execute("SELECT ID,NAME,DATE,FIRSTH,FIRSTL,SECONDH,SECONDL,STOCK_TYPE,ORDER_ID from Stocks")
    for row in cursor:
        print ("ID = ", row[0])
        print ("NAME = ", row[1])
        print ("DATE = ", row[2])
        print ("FIRSTH = ", row[3], "\n")
        print ("FIRSTL = ", row[4], "\n")
        print ("SECONDH = ", row[5], "\n")
        print ("SECONDL = ", row[6], "\n")
        print ("STOCK_TYPE = ", row[7], "\n")
        print ("ORDER_ID = ", row[8], "\n")

    if row[7] == 'BUY' :
        print("BUY")
        # check first low covering it is only works 9:31 to 3:00 so value is not second or first candle
        if value < row[4] :
            print('stop loss change to second low {}'.format(row[6]))
            # modify stoploss zerodha api call with order id
    else :
        print("SELL")
        if value > row[3] :
            print('stop loss change to second high {}'.format(row[5]))
             # modify stoploss zerodha api call with order id

def runScript():
    while True: 
        #add 14 to stop at 3
        if datetime.datetime.now().hour < 22  :
            nifty = yf.Ticker("%5ENSEI")
            print(nifty.info['regularMarketPrice'])
            jobChecker(nifty.info['regularMarketPrice'])
            time.sleep(20)
        else: 
            print("Stop zerodha trading with orderid now time 3")
            sys.exit()

runScript()       


