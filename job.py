import schedule
import time
import subprocess

def job(t):
    print ("I'm working..."), t
    subprocess.call("python dataloader.py 1", shell=True)
    return

schedule.every().day.at("09:35").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute


