import schedule
import time
import subprocess
from test import regenerateKey

def job(t):
    print ("I'm working..."), t

    subprocess.call("python dataloader.py 1", shell=True)
    regenerateKey(typeme='new')
    return

schedule.every().day.at("09:31").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


