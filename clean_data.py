#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# cleanING the data 
# removing commas, dashes, and non-numeric values


# In[ ]:


import os
import pandas as pd
import mplfinance as mpf

dir = 'C:/Users/shwet/OneDrive/Documents/InvestWise/Historical_Data'

ls_ = os.listdir(dir)
print(ls_)

ls = [f for f in ls_ if 'csv' in f]

for x in ls:
    df = pd.read_csv(f'{dir}/{x}')
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume']
    df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
    
    for col in df.columns:
        if col != 'Date':
            df[col] = df[col].astype(str).str.replace(',','').str.replace('-','')
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.to_csv(f'C:/Users/shwet/OneDrive/Documents/InvestWise/CleanedHistorical/{x}',index=False)
    print(x,'saved')


# In[ ]:




