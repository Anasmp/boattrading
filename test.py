import logging
from flask import Flask
app = Flask(__name__)
import os

logging.basicConfig(level=logging.DEBUG)


import sqlite3
conn = sqlite3.connect('data.db')
from kiteconnect import KiteConnect
kite = KiteConnect(api_key="yqw13acxnjzycwri")



def regenerateKey(typeme):
    if typeme == 'new':
        os.system("python3 zerodaAccess.py")
    query = "SELECT TOKEN from Stocks WHERE ID=(SELECT max(ID) FROM Stocks)"
    with conn:
        cursor = conn.execute(query);
        for row in cursor:
            print ("ID = ", row[0])
    conn.close()
    
    data = kite.generate_session(str(row[0]), api_secret="32f9wfuwq8dzlyyc6pt7dtpzex0a0836")
    kite.set_access_token(data["access_token"])
    print(row[0])
    


    

regenerateKey(typeme='new')




@app.route('/')
def hello_world():
    
    # try:
    #     order_id = kite.place_order(tradingsymbol="NIFTY 50",
    #                                 exchange="NSE",
    #                                 transaction_type="BUY",
    #                                 quantity=1,
    #                                 variety="co",
    #                                 order_type="MARKET",
    #                                 product="MIS",
    #                                 stoploss = "16567",
    #                                 validity="DAY"
    #                                 )

    #     logging.info("Order placed. ID is: {}".format(order_id))
    # except Exception as e:
    #     logging.info("Order placement failed: {}".format(e))
    
    return 'succcess'

# @app.route('/post')
# def hello_world2():
#     try:
#         order_id = kite.place_order(tradingsymbol="NIFTY 50",
#                                     exchange="NSE",
#                                     transaction_type="BUY",
#                                     quantity=1,
#                                     variety="regular",
#                                     order_type="MARKET",
#                                     product="CNC",
#                                     trigger_price = "16569",
#                                     stoploss = "16567"
#                                     )

#         logging.info("Order placed. ID is: {}".format(order_id))
#     except Exception as e:
#         logging.info("Order placement failed: {}".format(e))
    
#     return 'success'

logging.basicConfig(level=logging.DEBUG)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


