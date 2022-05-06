from fyers_api import accessToken, fyersModel

from selenium import webdriver
import time

from selenium.webdriver.common.by import By

import conf_reader
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


app_id = conf_reader.props["fyers_app_id"]
app_secret = conf_reader.props["fyers_app_secret"]
FYERS_ID = conf_reader.props["fyers_login_id"]
FYERS_PASSWORD = conf_reader.props["fyers_password"]
PANCARD = conf_reader.props["pancard"]

fyers = fyersModel.FyersModel(False)

def get_access_token( accessToken):
    from fyers_api import accessToken

    app_session = accessToken.SessionModel(client_id=app_id,
                                       secret_key=app_secret, redirect_uri="https://yogeshdewangan.com/123",
                                       response_type="code", grant_type="authorization_code")

    response = app_session.generate_authcode()

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(response)
    driver.find_element_by_id("fy_client_id").send_keys(FYERS_ID)
    driver.find_element_by_id("clientIdSubmit").click()
    time.sleep(1)
    driver.find_element_by_id("fy_client_pwd").send_keys(FYERS_PASSWORD)
    driver.find_element_by_id("loginSubmit").click()
    time.sleep(3)
    time.sleep(3)
    current_url = driver.current_url
    driver.quit()
    access_token = current_url.split("auth_code=")[1]
    return access_token


f= open("token.txt","r")
access_token = f.read()
if access_token == '':
    access_token = get_access_token(accessToken )
else:
    profile = fyers.get_profile()
    if profile["code"] != 200:
        access_token = get_access_token(accessToken)
f.close()


f= open("token.txt","w")
f.write(access_token)
f.close()


profile = fyers.get_profile()
print(str(profile))

funds = fyers.funds()
print(str(funds))





