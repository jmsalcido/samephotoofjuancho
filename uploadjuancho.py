#!/usr/bin/env python3

# We are going to run this, one time per day (I just dont want to... manually update the picture.)

import sys
import os
import getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_driverUrl = "http://facebook.com"
_facebookPage = "https://www.facebook.com/pages/The-same-photo-of-Juan-in-a-Sonic-costume-everyday/1549049825344078"
_file = "/Users/jsalcido/Desktop/stuff/sonic.jpg"

def initializeDriver(url):
    print("Starting driver at: " + _driverUrl)
    driver = webdriver.Chrome()
    driver.set_window_size(800,600)
    driver.get(url)
    return driver

def main():
    webDriver = initializeDriver(_driverUrl)
    login(webDriver)
    uploadImage(webDriver)
    post(webDriver)
    webDriver.quit()

def getUsernameAndPassword():
    return {'username': '', 'password': ''} # should obtain it from a properties file just for fun

def login(webDriver):
    loginData = getUsernameAndPassword()
    loginElement = findByCssSelector(webDriver, 'input[name="email"]')
    passwordElement = findByCssSelector(webDriver, 'input[name="pass"]')
    loginElement.send_keys(loginData["username"])
    passwordElement.send_keys(loginData["password"])
    print("Trying to log in...")
    findByCssSelector(webDriver, 'input[type="submit"]').click()
    webDriver.save_screenshot("login.png")

def findByCssSelector(webDriver, cssSelector):
    return webDriver.find_element(By.CSS_SELECTOR, cssSelector);

def uploadImage(webDriver):
    webDriver.get(_facebookPage)
    webDriver.implicitly_wait(10)
    findByCssSelector(webDriver, "a[data-endpoint*='composerx/attachment/media']").click()
    webDriver.implicitly_wait(3)
    upload = findByCssSelector(webDriver, "input[aria-label*='Upload Photos/Video']")
    upload.send_keys(_file)
    print("Uploading image...")

def post(webDriver):
    button = WebDriverWait(webDriver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Post']"))
    )
    message = getMessage(sys.argv[1:])
    print("POSTING PICTURE WITH MSG: " + message)
    # textArea = findByCssSelector(webDriver, 'textarea[title*="something"]')
    webDriver.implicitly_wait(2)
    # textArea.send_keys(message)
    button.click()

def getMessage(argv):
    args = {}
    defaultMessage = "Daily picture of Juan in a Sonic costume."
    try:
        opts, args = getopt.getopt(argv, "hm:",["message="])
    except:
        return defaultMessage
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            return arg
    return args;


if __name__ == "__main__":
    main()
