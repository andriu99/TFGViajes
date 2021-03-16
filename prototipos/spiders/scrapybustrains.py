# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 11:42:47 2021

@author: ANDRES
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random 
class BusTrainsScraper(scrapy.Spider):
    name = 'bustrainsspider'
    start_urls = ['https://www.thetrainline.com/es']
    allowed_domains=['thetrainline.com']
    booleanBus=False
    strdate=''
    def __init__(self,booleanBus,strdate):
        self.booleanBus=booleanBus
        self.strdate=strdate
    
    def getUrl(self):
        # opts = Options()
        # opts.add_argument("user-agent="+str(random.randrange(1,50)))

        driver = webdriver.Chrome()
        driver.get("https://www.thetrainline.com/es")
        driver.find_element_by_id("from.search").click()
        driver.find_element_by_id("from.search").clear()
        driver.find_element_by_id("from.search").send_keys("burgos")
        #driver.find_element_by_xpath("//li[@id='selected_option']/div/span").click()
        driver.find_element_by_id("to.search").click()
        driver.find_element_by_id("to.search").clear()
        driver.find_element_by_id("to.search").send_keys("madrid")
        #driver.find_element_by_xpath("//li[@id='selected_option']/div/span").click()
        driver.implicitly_wait(400)
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
        driver.delete_all_cookies()
        
        return driver.current_url

    def start_requests(self):
        url=self.getUrl()
        print(url)
        headers = {'User-Agent': 'AdsBot-Google (+http://www.google.com/adsbot.html)'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)
        
        

    def parse(self, response):
        print("Response:")
        print(response.txt)
  
if __name__=="__main__":
    process= CrawlerProcess()
    date=dt(2021,3,16)
    spider = BusTrainsScraper(True,str(date.isoformat()))
    process.crawl(BusTrainsScraper,True,str(date.isoformat()))
    process.start()


