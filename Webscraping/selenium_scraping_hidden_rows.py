# -*- coding: utf-8 -*-
"""
webscraping using selenium after clicking buttons

@author: Mayank
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

path = "C:\\Users\\Mayank\\OneDrive\\Udemy\\Quant Investing Using Python\\1.5_Web Scraping\\scripts\\chromedriver.exe"


### clicking dropdown buttons before scraping   
service = webdriver.chrome.service.Service(path)
service.start()

ticker = "AAPL"
url = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker,ticker)

driver = webdriver.Chrome(service=service)
driver.get(url)
driver.implicitly_wait(3) 

buttons = driver.find_elements(By.XPATH,  '//section[@data-test="qsp-financial"]//button')
for button in buttons:
    if button.accessible_name in ["Quarterly","Expand All"]:
        pass
    else:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable(button)).click()
        
income_st_dir = {}
table = driver.find_elements(By.XPATH,  "//*[@class='D(tbr) fi-row Bgc($hoverBgColor):h']")
table_heading = driver.find_elements(By.XPATH,  "//*[contains(@class, 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(ib) Fw(b)')]")
headings = []
for cell in table_heading:
    headings.append(cell.text)

for cell in table:
    [key, val] = cell.text.split("\n")
    income_st_dir[key] = val.split(" ")
    
income_statement_df = pd.DataFrame(income_st_dir).T
income_statement_df.columns = headings
        