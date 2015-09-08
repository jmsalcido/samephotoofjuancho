#!/usr/bin/env python3

import sys
import os
import getopt
import random
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# We are going to run this, one time per day (I just dont want to... manually update the picture.)
# URLs
_facebookUrl = "http://facebook.com"
_facebookPage = "https://www.facebook.com/pages/The-same-photo-of-Juan-in-a-Sonic-costume-everyday/1549049825344078"

# obtain the file picture that we will upload
_file = os.getcwd() + "/sonic.jpg"

# do not publish image, just upload it (testing purposes)
_postImage = True

_randomSentences = [
    "Daily picture of Juan in a Sonic costume.",
    "Juan is here, again!",
    "Almost got me.",
    "Juan is the king.",
    "Today is Juan day."
]

def initializeDriver(url):
    print("Starting driver at: " + url)
    driver = webdriver.Chrome()
    driver.set_window_size(800,600)
    driver.get(url)
    return driver

def main():
    webDriver = initializeDriver(_facebookUrl)
    login(webDriver)
    uploadImage(webDriver)
    postImage(webDriver)
    webDriver.implicitly_wait(10) # wait until post is done. (Slow internet, #1 should be this issue)
    webDriver.quit()

def getUsernameAndPassword():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return {'username': config['login']['username'], 'password': config['login']['password']}

def login(webDriver):
    loginData = getUsernameAndPassword()
    loginElement = findByCssSelector(webDriver, 'input[name="email"]')
    passwordElement = findByCssSelector(webDriver, 'input[name="pass"]')
    loginElement.send_keys(loginData["username"])
    passwordElement.send_keys(loginData["password"])
    print("Trying to log in...")
    findByCssSelector(webDriver, 'input[type="submit"]').click()

def findByCssSelector(webDriver, cssSelector):
    return webDriver.find_element(By.CSS_SELECTOR, cssSelector);

def uploadImage(webDriver):
    webDriver.get(_facebookPage)
    webDriver.implicitly_wait(10)
    message = getFacebookPostMessage(sys.argv[1:])
    print("Message used: " + message)
    textArea = findByCssSelector(webDriver, 'textarea[title*="something"]')
    textArea.send_keys(message)
    findByCssSelector(webDriver, "a[data-endpoint*='composerx/attachment/media']").click()
    webDriver.implicitly_wait(3)
    upload = findByCssSelector(webDriver, "input[aria-label*='Upload Photos/Video']")
    print("Uploading image: " + _file)
    upload.send_keys(_file)

def postImage(webDriver):
    button = WebDriverWait(webDriver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Post']"))
    )
    print("POSTING IMG!")
    if _postImage:
        button.click()

def getFacebookPostMessage(argv):
    args = {}
    defaultMessage = random.choice(_randomSentences)
    try:
        opts, args = getopt.getopt(argv, "m:",["message="])
    except:
        return defaultMessage
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            return arg
    return defaultMessage;


if __name__ == "__main__":
    main()
