#!/usr/bin/env python3

from selenium import webdriver

_driverUrl = "http://facebook.com"

def prepareDriver(url):
    driver = webdriver.PhantomJS()
    driver.set_window_size(800,600)
    driver.get(url)

def main():
    print("Starting driver at: " + _driverUrl)
    driver = prepareDriver(_driverUrl)

def uploadImage():
     pass

if __name__ == "__main__":
    main()
