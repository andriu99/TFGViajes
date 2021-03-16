# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from datetime import datetime as dt

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.headless = False
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.thetrainline.com/es")

        buttonCookies=driver.find_element_by_id("onetrust-accept-btn-handler")
        if buttonCookies!=None:
            buttonCookies.click()

        driver.find_element_by_id("from.search").click()
        driver.find_element_by_id("from.search").clear()
        driver.find_element_by_id("from.search").send_keys("Madrid")
        #driver.find_element_by_xpath("//ul[@id='stations_from']/div/li/div/span").click()
        driver.find_element_by_id("to.search").click()
        driver.find_element_by_id("to.search").clear()
        driver.find_element_by_id("to.search").send_keys("Barcelona")
        #driver.find_element_by_xpath("//ul[@id='stations_to']/div/li/div/span").click()
        driver.find_element_by_xpath("//button")
        driver.quit()
       
        print(driver.current_url)


    
    


if __name__ == "__main__":
    unittest.main()
