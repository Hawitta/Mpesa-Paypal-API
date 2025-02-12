from flask import Flask, request, render_template, jsonify
import requests
from requests.auth import HTTPBasicAuth
import base64
import datetime
import json
import paypalrestsdk
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
load_dotenv()

# M-Pesa credentials
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
shortcode = ''
passkey = os.getenv("PASSKEY")
callback_url = 'https://4d95-41-90-184-64.ngrok-free.app'


def generate_oauth_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']


def generate_password():
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8'), timestamp


def stk_push_request(phone_number, amount, transaction_type="CustomerPayBillOnline"):
    access_token = generate_oauth_token()
    password, timestamp = generate_password()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    payload = {
    "BusinessShortCode": 174379,  #paybill number
    "Password": os.getenv("DARAJA_PASSWORD"),
    "Timestamp": "20240724180856",
    "TransactionType": transaction_type,
    "Amount": amount,
    "PartyA": 254703961456,
    "PartyB": 174379, #paybill number
    "PhoneNumber": phone_number,
    "CallBackURL": callback_url,
    "AccountReference": "Bima Life Insurance",
    "TransactionDesc": "Payment of X" 
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@app.route('/')
def index():
    return render_template('index.html')

# END POINT FOR STK
@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    phone_number = data.get('phone_number')
    amount = data.get('amount')    
    transaction_type = data.get('transaction_type', "CustomerPayBillOnline")  # Default to "CustomerPayBillOnline"

    response = stk_push_request(phone_number, amount, transaction_type)

    # Log the transaction (for simplicity, we save to a file here. In a real app, save to a database)
    with open('transactions.log', 'a') as log_file:
        log_file.write(json.dumps(response) + '\n')

    return jsonify(response)


@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    # Log the callback data (for simplicity, we print it here. In a real app, save to database)
    print(data)
    with open('callback.log', 'a') as log_file:
        log_file.write(json.dumps(data) + '\n')
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})



@app.route("/success")
def onSuccess():
    return render_template("success.html")



@app.route("/fail")
def onFail():
    return render_template("fail.html")

# PayPal API Configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET")
})


# This method is run first when testing Paypal integration

@app.route('/create-payment', methods=['POST']) # receives amount from frontend framework
def create_payment():
    data = request.get_json()
    amount = data.get('amount', '10.00')  # Default to $10.00 if not provided

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": amount, "currency": "USD"},
            "description": "Insurance Payment"
        }],
        "redirect_urls": {
            "return_url": "https://4d95-41-90-184-64.ngrok-free.app/success",
            "cancel_url": "https://4d95-41-90-184-64.ngrok-free.app/fail"
        }
    })

    if payment.create():
        return jsonify({"status": "success", "approval_url": payment.links[1].href})
    else:
        return jsonify({"status": "error", "message": payment.error}), 400
    
    
# This is run after the payment has been initiated

# The payment_id and payer_id is received once the transaction has been sent to the merchant

    
@app.route('/execute-payment', methods=['POST'])
def execute_payment():
    data = request.get_json()
    payment_id = data.get('payment_id')
    payer_id = data.get('payer_id')

    
    if not payment_id or not payer_id:
        return jsonify({"status": "error", "message": "Missing payment_id or payer_id"}), 400
    
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return jsonify({"status": "success", "message": "Payment completed!"})
    else:
        return jsonify({"status": "error", "message": payment.error}), 400


if __name__ == '__main__':
    app.run(debug=True)
