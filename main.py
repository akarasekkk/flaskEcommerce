from flask import Flask, request
from datetime import datetime
import hmac
import hashlib
import requests
import json
import omise
from flask_cors import CORS

api_key = '3_M7WOpgvIytcpXYKaxLw9Qb10VERuiaaHaCy6O5ImaJzuUc1EzuBZdNctBqgw5x'
api_secret = '9896b3b29dd6a3b133ff5967572c6aeab27e2372d67a3e01398ff9c795b03ca3'


def get_time_stamp():
    return str(int(datetime.now().timestamp() * 1000 - 2000))


def get_signature(message):
    data = json.dumps(message, separators=(",", ":"))
    message = '{}{}'.format(get_time_stamp(), data)
    hash_ = hmac.new(b"9896b3b29dd6a3b133ff5967572c6aeab27e2372d67a3e01398ff9c795b03ca3", bytes(message, "utf-8"),
                     hashlib.sha256)
    hash_result = hash_.hexdigest()
    return hash_result


def get_signature_get():
    message = '{}'.format(get_time_stamp())
    hash_ = hmac.new(b"9896b3b29dd6a3b133ff5967572c6aeab27e2372d67a3e01398ff9c795b03ca3", bytes(message, "utf-8"),
                     hashlib.sha256)
    hash_result = hash_.hexdigest()
    return hash_result


def omise_charge(token, amount):
    omise.api_secret = "skey_test_5cavgpd6csnqyyzxxko"
    charge = omise.Charge.create(
        amount=amount,
        currency="USD",
        card=token,
        return_uri="https://www.omise.co/example_return_uri",
    )
    return charge.status


def get_product(product_id):
    data_json = open('products.json')
    response = json.load(data_json)
    for item in response:
        if product_id == item.get('id'):
            return item
    # d = {x['id']: x['name'] for x in data}
    # print(d)


def get_all_products():
    data_json = open('products.json')
    data = json.load(data_json)
    return data


def payment(amount):
    data = {
        "type": "without-conversion",
        "payment_amount": str(amount),
        "payment_currency": "USDT",
        "network": "BSC",
        "metadata": {
            "user_id": "jake01234"
        }
    }
    response = post_api('https://testnet.hashpays.io/api/crypto/payments', data)
    data = json.loads(response)
    print(data.get('id'))
    return 'ok'


def get_asset_api():
    get_api('https://testnet.hashpays.io/api/assets')


def check_status(payment_id):
    response = get_api('https://testnet.hashpays.io/api/crypto/payments' + payment_id)
    data = json.loads(response)
    print(data.get('status'))


def post_api(url, data):
    response = requests.post(url, json=data, headers={
        "Content-Type": "application/json",
        "User-Agent": "*",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "HASHPAYS-TIMESTAMP": get_time_stamp(),
        "HASHPAYS-API-KEY": api_key,
        "HASHPAYS-SIGNATURE": get_signature(data)
    })
    print(response.text)
    return response.text


def get_api(url):
    response = requests.get(url, headers={
        "Content-Type": "application/json",
        "User-Agent": "*",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "HASHPAYS-TIMESTAMP": get_time_stamp(),
        "HASHPAYS-API-KEY": api_key,
        "HASHPAYS-SIGNATURE": get_signature_get()
    })

    print(response.text)
    return response.text


def ping():
    url = 'https://testnet.hashpays.io/api/ping'
    myobj = {"message": "ping"}
    print(get_time_stamp())
    response = requests.post(url, json=myobj, headers={
        "Content-Type": "application/json",
        "User-Agent": "*",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "HASHPAYS-TIMESTAMP": get_time_stamp(),
        "HASHPAYS-API-KEY": api_key,
        "HASHPAYS-SIGNATURE": get_signature(myobj)
    })

    print(response.request.url)
    print(response.request.headers)
    print(response.request.body)

    print(response.text)


app = Flask(__name__)
CORS(app)


@app.route("/products", methods=['GET'])
def products():
    return get_all_products()


@app.route('/product/<product_id>')
def profile(product_id):
    return get_product(product_id)


@app.route('/payment', methods=['POST'])
def payment_credit():
    print(request.json['email'])
    print(request.json['amount'][0])
    return omise_charge(request.json['token'], request.json['amount'][0])


@app.route('/payment-crypto', methods=['POST'])
def payment_credit_crypto():
    print(request.json['email'])
    print(request.json['amount'][0])
    return payment(request.json['amount'][0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# get_all_products()
# get_product('1')
# ping()
# get_asset_api()
