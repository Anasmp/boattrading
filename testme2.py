from datetime import datetime,timedelta

print(datetime.now() - timedelta(2))
#...some code...
if ( datetime.now() - (datetime.now() - timedelta(2)) ).days > 1:
    print('24 hours have passed')
else:
    print('Date is within 24 hours!')