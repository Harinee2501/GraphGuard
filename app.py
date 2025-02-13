from flask import Flask, render_template, request, jsonify
import json
from graph import FraudDetection

app = Flask(__name__)


fraud_system = FraudDetection()

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/upload', methods=['POST'])
def upload_transactions():

    data = request.form['transactions'] 
    

    try:
        transactions = json.loads(data) 
        for transaction in transactions:
            fraud_system.add_transaction(transaction['sender'], transaction['receiver'], transaction['amount'])
        results = fraud_system.detect_fraud()  
    except Exception as e:
        results = f"Error processing data: {e}"

    return render_template('result.html', results=results)

@app.route('/api/risk_score', methods=['POST'])
def risk_score():
    data = request.get_json()
    score = fraud_system.predict_risk(data)
    return jsonify({'risk_score': score})

if __name__ == "__main__":
    app.run(debug=True)


