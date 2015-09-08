#!/usr/bin/env python3

import sys
import os
import getopt
import random
import configparser
import time
import datetime
import calendar
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

# dateFormat @facebook last post
# dayOfWeek, month dayOfMonth, year
# somecharacterswhonoonecares(timeandotherstuff)
_dateFormat = "{0}, {1} {2}, {3}"

_randomSentences = [
    "Daily picture of Juan in a Sonic costume.",
    "Juan is here, again!",
    "Almost got me.",
    "Juan is the king.",
    "Today is Juan day.",
    "Juan fact number 54: he uses his sonic costume for the ladies."
]


def main():
    webDriver = initializeDriver(_facebookUrl)
    login(webDriver)
    uploadImage(webDriver)
    postImage(webDriver)
    # webDriver.implicitly_wait(30) # wait until post is done. (Slow internet,
    # #1 should be this issue)
    webDriver.quit()


def initializeDriver(url):
    webDriver = webdriver.Chrome()  # 2 use phantomjs instead of chrome
    webDriver.set_window_size(800, 600)
    goToPage(webDriver, _facebookUrl)
    return webDriver


def getUsernameAndPassword():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return {
        'username': config['login']['username'],
        'password': config['login']['password']
    }


def login(webDriver):
    loginData = getUsernameAndPassword()
    loginElement = findLoginElement(webDriver)
    passwordElement = findPasswordElement(webDriver)
    sendKeys(loginElement, loginData["username"])
    sendKeys(passwordElement, loginData["password"])
    clickOn(findLoginButtonElement(webDriver))
    waitForElement(webDriver, 30, 'a[title="Profile"]')


def uploadImage(webDriver):
    imageCssSelector = "a[data-endpoint*='composerx/attachment/media']"
    goToPage(webDriver, _facebookPage)
    imageElement = waitForElement(webDriver, 30, imageCssSelector)
    setPostMessage(webDriver)
    clickOn(imageElement)
    upload = waitForElement(
        webDriver, 30, "input[aria-label*='Upload Photos/Video']")
    sendKeys(upload, _file)


def setPostMessage(webDriver):
    message = getFacebookPostMessage(getArgs())
    textArea = findByCssSelector(webDriver, 'textarea[title*="something"]')
    sendKeys(textArea, message)


def postImage(webDriver):
    button = waitForElement(webDriver, 30, "button[aria-label='Post']")
    if _postImage:
        clickOnPublishButton(webDriver, button)


def clickOnPublishButton(webDriver, buttonElement):
    clickOn(buttonElement)
    cssSelectorForPublishedPost = "abbr[title*='" + \
        getFormatedDate(datetime.date.today()) + "']"
    waitForElement(webDriver, 30, cssSelectorForPublishedPost)


def getFormatedDate(dateTime):
    weekdayName = calendar.day_name[dateTime.weekday()]
    monthName = calendar.month_name[dateTime.month]
    return _dateFormat.format(weekdayName, monthName, dateTime.day, dateTime.year)


def getArgs():
    return sys.argv[1:]


def getFacebookPostMessage(argv):
    args = {}
    defaultMessage = random.choice(_randomSentences)
    try:
        opts, args = getopt.getopt(argv, "m:", ["message="])
    except:
        return defaultMessage
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            return arg
    return defaultMessage


def findLoginElement(webDriver):
    return findByCssSelector(webDriver, 'input[name="email"]')


def findPasswordElement(webDriver):
    return findByCssSelector(webDriver, 'input[name="pass"]')


def findLoginButtonElement(webDriver):
    return findByCssSelector(webDriver, 'input[type="submit"]')


def findByCssSelector(webDriver, cssSelector):
    return webDriver.find_element(By.CSS_SELECTOR, cssSelector)


def sendKeys(element, value):
    element.clear()
    element.send_keys(value)


def clickOn(element):
    element.click()


def waitForElement(webDriver, timeOut, cssSelector):
    return WebDriverWait(webDriver, timeOut).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cssSelector))
    )


def goToPage(webDriver, url):
    webDriver.get(url)

if __name__ == "__main__":
    main()
