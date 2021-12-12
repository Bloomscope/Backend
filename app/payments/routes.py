from flask import Blueprint, render_template, request, jsonify
import razorpay
from ..config import RAZOR_PAY_ID, RAZOR_PAY_SECRET


payment = Blueprint('payment', __name__)
client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))


@payment.route('/html')
def html():
    return render_template('test.html', key=RAZOR_PAY_ID)

@payment.route('/test')
def test():
    DATA = {
    "amount": 100,
    "currency": "INR",
    "receipt": "receipt#1",
    }
    resp = client.order.create(data=DATA)
    return jsonify(resp)


@payment.route('/verify', methods=['POST'])
def verify():
    params_dict = request.get_json(force=True)
    print(params_dict)
    is_ok = client.utility.verify_payment_signature(params_dict)
    print(is_ok)
    return is_ok