# Mpesa & PayPal Payment API

## Overview
This project is an API that integrates M-Pesa and PayPal payment processing. It allows users to initiate transactions via M-Pesa STK Push and PayPal payments, ensuring a seamless payment experience.

## Features
- **M-Pesa STK Push**: Users can pay via Safaricom's M-Pesa using STK Push.
- **PayPal Integration**: Users can make payments through PayPal.
- **Webhook Support**: Receives payment confirmation callbacks from M-Pesa and PayPal.
- **RESTful API Endpoints**: Supports JSON-based communication.
- **Logging and Error Handling**: Logs transaction details and errors for debugging.

## Technologies Used
- **Backend**: Flask (Python) for M-Pesa and PayPal transaction processing.
- **Frontend (if applicable)**: Ruby on Rails API for handling payment requests.
- **Database**: PostgreSQL/MySQL (Optional for storing transactions).
- **APIs**:
  - M-Pesa Daraja API
  - PayPal REST API
- **Deployment**: Ngrok for local API tunneling, Heroku/AWS for production.

## Installation & Setup
### Prerequisites
- Python 3.8+
- Flask
- Ruby on Rails
- Ngrok (for local testing)
- A registered Safaricom M-Pesa Daraja API account
- A PayPal Developer account

### Clone the Repository
```bash
git clone https://github.com/Hawitta/Mpesa-Paypal-API.git
cd Mpesa-Paypal-API
```

### Setup Environment Variables
Create a `.env` file in the project root and add the following:
```ini
# M-Pesa Credentials
MPESA_CONSUMER_KEY=your_mpesa_consumer_key
MPESA_CONSUMER_SECRET=your_mpesa_consumer_secret
MPESA_PASSKEY=your_mpesa_passkey
MPESA_SHORTCODE=your_mpesa_shortcode
CALLBACK_URL=https://your-ngrok-url/mpesa/callback

# PayPal Credentials
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_SECRET=your_paypal_secret
PAYPAL_MODE=sandbox  # Use 'live' in production
```

### Install Dependencies
For Flask:
```bash
pip install -r requirements.txt
```
For Rails:
```bash
bundle install
```

## Running the Application
Start the Flask API:
```bash
python app.py
```
Start the Rails API:
```bash
rails server
```

## API Endpoints
### 1. M-Pesa Payment
**Initiate STK Push**
```http
POST /subscribe
```
**Request Body:**
```json
{
  "phone_number": "254712345678",
  "amount": 100
}
```

### 2. PayPal Payment
**Create PayPal Payment**
```http
POST /create-payment
```
**Request Body:**
```json
{
  "amount": 50.00
}
```

**Execute PayPal Payment**
```http
POST /execute-payment
```
**Request Body:**
```json
{
  "payment_id": "PAY-12345678",
  "payer_id": "PAYER-987654"
}
```

## Testing with Ngrok & ThunderClient
1. Start Ngrok:
   ```bash
   ngrok http 5000
   ```
2. Use the Ngrok URL in your `.env` file.
3. Use ThunderClient/Postman to test API endpoints.

## Deployment
For production, deploy the Flask API to Heroku or AWS Lambda and the Rails API to a cloud server.

## License
This project is open-source and available under the MIT License.

## Contributors
- **Hawiana Abebe Bedada** ([@Hawitta](https://github.com/Hawitta))

