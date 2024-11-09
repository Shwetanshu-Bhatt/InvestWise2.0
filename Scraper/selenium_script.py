#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from bs4 import BeautifulSoup


# In[ ]:


stock_names = [
    "HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS", "AXISBANK.NS", "PNB.NS",
    "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS", "COFORGE.NS",
    "RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "BPCL.NS", "IOC.NS",
    "ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS", "DABUR.NS", "MARICO.NS",
    "SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "AUROPHARMA.NS", "BIOCON.NS",
    "MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "HEROMOTOCO.NS", "ASHOKLEY.NS",
    "TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "COALINDIA.NS",
    "DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PHOENIXLTD.NS", "BRIGADE.NS",
    "BHARTIARTL.NS", "IDEA.NS", "RELIANCE.NS",
    "ASIANPAINT.NS", "PIDILITIND.NS", "VOLTAS.NS", "HAVELLS.NS", "BAJAJELEC.NS"
]


# In[ ]:


options = webdriver.EdgeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--disable-images")
options.add_argument("--window-size=1920,1080")


# In[ ]:


driver = webdriver.Edge(options=options)


# In[ ]:


for name in stock_names:
    url = f"https://finance.yahoo.com/quote/{name}/history/?period1=0&period2=1728399828"
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_element_located((By.XPATH, "//table")))
    table_html = driver.execute_script("return arguments[0].outerHTML;", table)
    soup = BeautifulSoup(table_html, "html.parser")
    headers = [header.text for header in soup.find_all("th")]
    rows = soup.find("tbody").find_all("tr")
    data = []
    for row in tqdm(rows, desc=f"Processing rows for {name}", unit="row"):
        cols = [col.get("data-real-value", col.text) for col in row.find_all("td")]
        if cols:
            data.append(cols)
    csv_path = os.path.join(f'{name}.csv')
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Data for {name} saved to {name}.csv")

driver.quit()


# In[ ]:




