# import datetime
from datetime import datetime
from numpy.lib.type_check import typename
import pandas as pd
import sqlite3
import subprocess
import time  

import sys
import os

df = pd.read_csv('data_file.csv')
conn = sqlite3.connect('data.db')


# conn.execute('''CREATE TABLE Stocks
#          (ID INTEGER PRIMARY KEY,
#          NAME           TEXT    NOT NULL,
#          DATE           DATETIME     NOT NULL,
#          FIRSTH        REAL,
#          FIRSTL        REAL,
#          SECONDH        REAL,
#          SECONDL        REAL,
#          CURRENT         REAL);''')


# conn.close()

df['date'] = pd.DatetimeIndex(df['date'])
# datetime.today().strftime('%Y-%m-%d')
df = df[df['date'].dt.strftime('%Y-%m-%d') == '2021-08-18']
df = pd.DataFrame(df)

# print(len(df))


def runSuperScript(target,stoploss,typeme):


    if typeme == "BUY" :
        print(target,stoploss,'buy')
        #background process with nohup
        os.system("python3 job2.py")
        # zerodha api request for buy order

    elif typeme == "SELL" :
        print(target,stoploss,'sell')
        #background process with nohup
        os.system("nohup python3 job2.py &")
        #zerodha api request for sell order


if len(df) > 0 :
    df = df.set_index(df['date'])

    first = df.between_time('15:00', '15:00')
    second = df.between_time('15:15', '15:30')


    firstH = first.iloc[0]['high']
    firstL = first.iloc[0]['low']
    secondH = second.iloc[0]['high']
    secondL = second.iloc[0]['low']


    print('First candle highest',firstH)
    print('First candle Lowest',firstL)


    print('Second candle highest',secondH)
    print('Second candle Lowest',secondL)

 
    if (secondH > firstH) :
        print ('place sell order with trigger price {} and stoploss {}'.format(secondL,firstH))
        with conn:
            conn.execute("INSERT INTO Stocks (ID,NAME,DATE,FIRSTH,FIRSTL,SECONDH,SECONDL,CURRENT,STOCK_TYPE) \
            VALUES (NULL,'Nifty', ?, ?, ?, ?,?,NULL,'SELL' )",[time.strftime('%Y-%m-%d %H:%M:%S'),firstH,firstL,secondH,secondL] );
        conn.close()
        runSuperScript(secondL,firstH,typeme="SELL")    
    elif (secondL < firstL) :
        print ('place buy order with trigger price {} and stoploss {}'.format(secondH,firstL))
        with conn:
            conn.execute("INSERT INTO Stocks (ID,NAME,DATE,FIRSTH,FIRSTL,SECONDH,SECONDL,CURRENT,STOCK_TYPE) \
            VALUES (NULL,'Nifty', ?, ?, ?, ?,?,NULL,'BUY' )",[time.strftime('%Y-%m-%d %H:%M:%S'),firstH,firstL,secondH,secondL] );
        conn.close()
        runSuperScript(secondL,firstH,typeme="BUY")
    else:
        print('condition not satisfied')
        sys.exit()


else:
    print('no trading today')



