from flask import Flask, render_template, request
import joblib
import pickle
from numpy.testing._private.utils import IgnoreException
import pandas as pd

app = Flask(__name__)
data = pd.read_csv('df_model.csv')

#halaman home
@app.route('/')
def home():
    return render_template('home.html')

#halaman dataset
@app.route('/dataset', methods=['GET'])
def dataset():
    rows = list(data.values)
    header = list(data.columns)
    return render_template('dataset.html',rows=rows,header=header)

# #halaman visualisasi
@app.route('/visualize', methods=['POST', 'GET'])
def visual():
    return render_template('plot.html')

# #halaman input prediksi
@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    return render_template('predict.html')

# #halaman hasil prediksi
@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        input = request.form

        print(input)

        df_model_pred = pd.DataFrame({
            'ROA(A)_before_interest_and_%_after_tax': [float(input['ROA(A)_before_interest_and_%_after_tax'])],
            'Persistent_EPS_in_the_Last_Four_Seasons': [float(input['Persistent_EPS_in_the_Last_Four_Seasons'])],
            'Per_Share_Net_profit_before_tax_(Yuan_¥)': [float(input['Per_Share_Net_profit_before_tax_(Yuan_¥)'])],
            'Debt_ratio_%': [float(input['Debt_ratio_%'])],
            'Net_worth/Assets': [float(input['Net_worth/Assets'])],
            'Borrowing_dependency': [float(input['Borrowing_dependency'])],
            'Net_profit_before_tax/Paid-in_capital': [float(input['Net_profit_before_tax/Paid-in_capital'])],
            'Net_Income_to_Total_Assets': [float(input['Net_Income_to_Total_Assets'])],
            "Net_Income_to_Stockholder's_Equity": [float(input["Net_Income_to_Stockholder's_Equity"])]
        })

        print(df_model_pred)


        prediksi = model.predict_proba(df_model_pred)[0][1]

        if prediksi > 0.5:
            condition = "Survive"
        else:
            condition = "Bankrupt"

        return render_template('result.html',
            data=input, pred=condition)

if __name__ == '__main__':
    # model = joblib.load('model_joblib')

    filename = 'Bankruptcy.sav'
    model = pickle.load(open(filename,'rb'))

    app.run(debug=True)