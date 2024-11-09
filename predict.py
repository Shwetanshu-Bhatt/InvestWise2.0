import pandas as pd
import joblib

def get_user_data():
    open_prices = []
    close_prices = []
    
    days = int(input("Enter the number of days (at least 5): "))
    
    if days < 5:
        print("Please enter data for at least 5 days.")
        return get_user_data()
    
    for i in range(days):
        open_price = float(input(f"Enter the Open price for day {i+1}: "))
        close_price = float(input(f"Enter the Close price for day {i+1}: "))
        open_prices.append(open_price)
        close_prices.append(close_price)
    
    new_data = pd.DataFrame({
        'Open': open_prices[::-1],  
        'Close': close_prices[::-1]   
    })
    
    return new_data

def prepare_data(df):
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()  
    X = df[['Prev_Open', 'Prev_Close']]
    y = df[['Open', 'Close']]
    return X, y

general_model = joblib.load('general_linear_model.pkl')

new_data = get_user_data()

new_X, _ = prepare_data(new_data)

predictions = general_model.predict(new_X)
print(predictions[-1])
