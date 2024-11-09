#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import joblib


# In[4]:


def prepare_data(df):
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()  
    X = df[['Prev_Open', 'Prev_Close']]
    y = df[['Open', 'Close']]
    return X, y


# In[3]:


folder_path = 'CleanedHistorical'  

general_model = LinearRegression()


# In[4]:


for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        
        X, y = prepare_data(df)
        
        general_model.fit(X, y)

print("Training complete on all files.")

joblib.dump(general_model, 'general_linear_model.pkl')
print("General model saved as 'general_linear_model.pkl'")

