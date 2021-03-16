# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://www.renfe.com/es/es")
        driver.find_element_by_xpath("//input[@id='origin']").click()
        driver.find_element_by_xpath("//input[@id='origin']").clear()
        driver.find_element_by_xpath("//input[@id='origin']").send_keys("BURGOS")
        try:
            driver.find_element_by_id("awesomplete_list_1_item_0").click()
        except: 
            driver.find_element_by_id("awesomplete_list_2_item_0").click()

        driver.find_element_by_xpath("//input[@id='destination']").click()
        driver.find_element_by_xpath("//input[@id='destination']").clear()
        driver.find_element_by_xpath("//input[@id='destination']").send_keys("BARCELONA")
        driver.find_element_by_xpath("//li[@id='awesomplete_list_2_item_0']/mark").click()
        print("BARCELONA")

        driver.find_element_by_xpath("//rf-select[@id='tripType']/div/button").click()
        driver.find_element_by_xpath("//rf-select[@id='tripType']/div/div/ul/li/button").click()
        print("Selector tipo viaje ")

        # driver.find_element_by_xpath("(//input[@type='text'])[5]").click()
        # driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        # driver.find_element_by_xpath("//div[@id='contentPage']/div/div/div/div/div/div/div/div/div/rf-header/rf-header-top/div[2]/rf-search/div/div[2]/div[2]/div[2]/form/rf-button/div/button/div[2]").click()
       
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
