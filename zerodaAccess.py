from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib.parse as urlparse
from selenium.webdriver.chrome.options import Options



class ZerodhaAccessToken:
    def __init__(self):
        self.apiKey = 'yqw13acxnjzycwri'
        self.apiSecret = '32f9wfuwq8dzlyyc6pt7dtpzex0a0836'
        self.accountUserName = 'QK0591'
        self.accountPassword = 'Salva@123'
        self.securityPin = '920744'

    def getaccesstoken(self):
        try:
            login_url = "https://kite.trade/connect/login?v=3&api_key={apiKey}".format(apiKey=self.apiKey)
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=options)

            driver.get(login_url)

            wait = WebDriverWait(driver, 20)

            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]')))\
                .send_keys(self.accountUserName)

            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))\
                .send_keys(self.accountPassword)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))\
                .submit()

            wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).click()
            time.sleep(5)
            driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.securityPin)

            wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).submit()


            wait.until(EC.url_contains('status=success'))

            ## get the token url after success
            tokenurl = driver.current_url
            parsed = urlparse.urlparse(tokenurl)
            driver.close()
            return urlparse.parse_qs(parsed.query)['request_token'][0]
        except Exception as ex:
            print(ex)


_ztoken = ZerodhaAccessToken()
actual_token = _ztoken.getaccesstoken()

import sqlite3
conn = sqlite3.connect('data.db')
query = "UPDATE Stocks SET TOKEN = '{}' WHERE ID=(SELECT max(ID) FROM Stocks)".format(str(actual_token))
with conn:
    cursor = conn.execute(query);

conn.close()

