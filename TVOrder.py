import json
import configparser
import fxcmAPI


def tradingview(data):
    try:
        data['passphrase']
    except:
        return {"code": "error",
                "message": "Nice try"}

    if (passwordVerify(data['passphrase'])):
        return {"code": "error",
                "message": "Nice try"}
    else:
        msg = fxcmAPI.fxcm(data)
        return msg


def passwordVerify(password):
    config = configparser.ConfigParser()
    config.read("./config.cfg")
    if (password != config['TradingView']['WEBHOOK_PASSPHRASE']):
        return True
    else:
        return False
