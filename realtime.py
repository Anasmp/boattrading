from websocket import create_connection
import json
import random
import string
import re
import pandas as pd
import csv
from datetime import datetime,timedelta

def filter_raw_message(text):
    try:
        found = re.search('"m":"(.+?)",', text).group(1)
        found2 = re.search('"p":(.+?"}"])}', text).group(1)
        print(found)
        print(found2)
        return found1, found2
    except AttributeError:
        print("error")
    

def generateSession():
    stringLength=12
    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(stringLength))
    return "qs_" +random_string

def generateChartSession():
    stringLength=12
    letters = string.ascii_lowercase
    random_string= ''.join(random.choice(letters) for i in range(stringLength))
    return "cs_" +random_string

def prependHeader(st):
    return "~m~" + str(len(st)) + "~m~" + st

def constructMessage(func, paramList):
    #json_mylist = json.dumps(mylist, separators=(',', ':'))
    return json.dumps({
        "m":func,
        "p":paramList
        }, separators=(',', ':'))

def createMessage(func, paramList):
    return prependHeader(constructMessage(func, paramList))

def sendRawMessage(ws, message):
    ws.send(prependHeader(message))

def sendMessage(ws, func, args):
    ws.send(createMessage(func, args))

def generate_csv(a):
    out= re.search('"s":\[(.+?)\}\]', a).group(1)
    x=out.split(',{\"')
    
    with open('realtime.csv', mode='w', newline='') as data_file:
        employee_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
        employee_writer.writerow(['index', 'date', 'open', 'high', 'low', 'close', 'volume'])
        
        for xi in x:
            xi= re.split('\[|:|,|\]', xi)
            print(xi)
            ind= int(xi[1]) 
            ts= datetime.fromtimestamp(float(xi[4]))
            ts = ts.strftime("%Y-%m-%d %H:%M:%S")
    
            employee_writer.writerow([ind, ts, float(xi[5]), float(xi[6]), float(xi[7]), float(xi[8]), float(xi[9])])
            


headers = json.dumps({
    'Origin': 'https://data.tradingview.com'
})


ws = create_connection(
    'wss://data.tradingview.com/socket.io/websocket',headers=headers)

session= generateSession()
print("session generated {}".format(session))

chart_session= generateChartSession()
print("chart_session generated {}".format(chart_session))


sendMessage(ws, "set_auth_token", ["unauthorized_user_token"])
sendMessage(ws, "chart_create_session", [chart_session, ""])
sendMessage(ws, "quote_create_session", [session])
sendMessage(ws,"quote_set_fields", [session,"ch","chp","current_session","description","local_description","language","exchange","fractional","is_tradable","lp","lp_time","minmov","minmove2","original_name","pricescale","pro_name","short_name","type","update_mode","volume","currency_code","rchp","rtc"])
sendMessage(ws, "quote_add_symbols",[session, "BINANCE:BTCUSDT", {"flags":['force_permission']}])
sendMessage(ws, "quote_fast_symbols", [session,"BINANCE:BTCUSDT"])

# st='~m~140~m~{"m":"resolve_symbol","p":}'
# p1, p2 = filter_raw_message(st)
sendMessage(ws, "resolve_symbol", [chart_session,"symbol_1","={\"symbol\":\"BINANCE:BTCUSDT\",\"adjustment\":\"splits\",\"session\":\"extended\"}"])
sendMessage(ws, "create_series", [chart_session, "s1", "s1", "symbol_1", "1", 50])

# Printing all the result

a=""
while True:
    try:
        result = ws.recv()

        try:
            out= re.search('"s":\[(.+?)\}\]', a).group(1)
            last = "[",out+"}]"
            print(result)
            break;
        except AttributeError:
            out= re.search('"s":\[(.+?)\}\]', a)
        
        # if result == '~m~4~m~~h~1' :
        #     break

        a=a+result+"\n"
      

    except Exception as e:
        print(e)
        break
# out= re.search('"s":\[(.+?)\}\]', a).group(1)
# print(out)
# x=out.split(',{\"')
# xi= re.split('\[|:|,|\]', x[0])
generate_csv(a)


