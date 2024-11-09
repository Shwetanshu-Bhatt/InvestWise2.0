#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import joblib


# In[2]:


def prepare_data(df):
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()  
    X = df[['Prev_Open', 'Prev_Close']]
    y = df[['Open', 'Close']]
    return X, y


# In[3]:


general_model = joblib.load('general_linear_model.pkl')

new_data = pd.DataFrame({
    'Open': [2960.00, 2967.90, 2864.00, 2803.00, 2701.10][::-1],  
    'Close': [2949.50, 2947.25, 2969.30, 2848.60, 2798.65][::-1]   
})
new_X, _ = prepare_data(new_data)

predictions = general_model.predict(new_X)
print(predictions[-1]) 


# In[ ]:




