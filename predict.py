from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

general_model = joblib.load('general_linear_model.pkl')

def prepare_data(df):
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()  
    X = df[['Prev_Open', 'Prev_Close']]
    y = df[['Open', 'Close']]
    return X, y

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        open_prices = list(map(float, data.get('open_prices', [])))
        close_prices = list(map(float, data.get('close_prices', [])))

        if len(open_prices) < 5 or len(close_prices) < 5:
            return jsonify({'error': 'Please provide data for at least 5 days'}), 400
        
        new_data = pd.DataFrame({
            'Open': open_prices[::-1],  
            'Close': close_prices[::-1]   
        })

        new_X, _ = prepare_data(new_data)

        predictions = general_model.predict(new_X)

        predicted_open = predictions[-1][0]
        predicted_close = predictions[-1][1]

        return jsonify({'predicted_open': predicted_open, 'predicted_close': predicted_close})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
