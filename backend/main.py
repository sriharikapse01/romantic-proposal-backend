from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import razorpay
import hmac
import hashlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

RAZORPAY_KEY_ID = "YOUR_TEST_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_TEST_KEY_SECRET"
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.post("/create-order/")
async def create_order(request: Request):
    data = await request.json()
    amount = 100 * 100
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
        "notes": data
    })
    return {
        "order_id": order["id"],
        "amount": amount,
        "currency": "INR",
        "razorpay_key_id": RAZORPAY_KEY_ID
    }

@app.post("/verify-payment/")
async def verify_payment(request: Request):
    data = await request.json()
    signature = hmac.new(
        bytes(RAZORPAY_KEY_SECRET, 'utf-8'),
        bytes(data['razorpay_order_id'] + "|" + data['razorpay_payment_id'], 'utf-8'),
        hashlib.sha256
    ).hexdigest()

    if signature == data['razorpay_signature']:
        return {"status": "success"}
    else:
        return {"status": "failure"}
