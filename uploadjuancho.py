#!/usr/bin/env python3

# We are going to run this, one time per day (I just dont want to... manually update the picture.)

from selenium import webdriver

_driverUrl = "http://facebook.com"
_facebookPage = "https://www.facebook.com/pages/The-same-photo-of-Juan-in-a-Sonic-costume-everyday/1549049825344078"

def initializeDriver(url):
    print("Starting driver at: " + _driverUrl)
    driver = webdriver.PhantomJS()
    driver.set_window_size(800,600)
    driver.get(url)
    return driver

def main():
    webDriver = initializeDriver(_driverUrl)
    login(webDriver)
    uploadImage(webDriver)
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
    return webDriver.find_element_by_css_selector(cssSelector);

def uploadImage(webDriver):
    webDriver.get(_facebookPage)
    findByCssSelector(webDriver, "a[data-endpoint*='composerx/attachment/media']")
    webDriver.save_screenshot("juancho.png")

if __name__ == "__main__":
    main()
