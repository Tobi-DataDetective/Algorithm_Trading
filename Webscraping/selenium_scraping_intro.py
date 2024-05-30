# -*- coding: utf-8 -*-
"""
webscraping using selenium

@author: Mayank
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

path = "C:\\Users\\Mayank\\OneDrive\\Udemy\\Quant Investing Using Python\\1.5_Web Scraping\\scripts\\chromedriver.exe"

service = webdriver.chrome.service.Service(path)
service.start()

ticker = "AAPL"
url = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker,ticker)

driver = webdriver.Chrome(service=service)
driver.get(url)
driver.implicitly_wait(3)

table = driver.find_element(By.XPATH,  '//div[@class="M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"]').text
print(table)
table_list = table.split("\n")
income_st_dir = {}
for count,i in enumerate(table_list):
    if count%2==0:
        if table_list[count] == "Breakdown":
            pass
        else:
            income_st_dir[i] = []
    else:
        if table_list[count-1] == "Breakdown":
            pass
        else:            
            income_st_dir[table_list[count-1]] = i.split("\t")
        

### 2nd way   (better, handles heading as well)  
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