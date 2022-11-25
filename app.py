from flask import Flask, request
import json
from module import fxcmAPI, TVOrder

app = Flask(__name__)

fxcmAPI.fxcmConnect()


@app.route('/webhook', methods=['POST'])
def main():

    data = json.loads(request.data)
    msg = TVOrder.tradingview(data)

    return msg


@app.route('/fxcmcheck', methods=['POST'])
def checkConnect():
    msg = fxcmAPI.checkConnect()
    return msg


if __name__ == "__main__":
    app.run()
