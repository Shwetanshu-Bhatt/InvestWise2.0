from flask import Flask, render_template, request, flash
import pandas as pd
import joblib

app = Flask(__name__)

def prepare_data(df):
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df = df.dropna()  
    X = df[['Prev_Open', 'Prev_Close']]
    y = df[['Open', 'Close']]
    return X, y

# Loading the model and checking if it loads correctly
try:
    general_model = joblib.load('general_linear_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    general_model = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the open and close prices from the form
        open_prices = request.form.get("open_prices").split(',')
        close_prices = request.form.get("close_prices").split(',')

        # Check if the user has entered at least 5 data points
        if len(open_prices) < 5 or len(close_prices) < 5:
            flash("You must enter at least 5 days of data for both open and close prices.", "error")
            return render_template("index.html")

        try:
            # Convert the inputs to floats and reverse the list to match the format (most recent first)
            open_prices = [float(price.strip()) for price in open_prices[::-1]]
            close_prices = [float(price.strip()) for price in close_prices[::-1]]
        except ValueError as e:
            flash(f"Invalid input: {e}", "error")
            return render_template("index.html")

        # Prepare the new data for prediction
        new_data = pd.DataFrame({
            'Open': open_prices,
            'Close': close_prices
        })

        # Prepare data for prediction
        new_X, _ = prepare_data(new_data)

        # Check if model is loaded successfully
        if general_model:
            try:
                # Make the prediction
                predictions = general_model.predict(new_X)
                predicted_open = predictions[-1][0]
                predicted_close = predictions[-1][1]
                return render_template("index.html", predicted_open=predicted_open, predicted_close=predicted_close)
            except Exception as e:
                flash(f"Prediction error: {e}", "error")
                return render_template("index.html")
        else:
            flash("Model is not available.", "error")
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
