import fxcmpy
import math
import time
import json


def fxcmConnect():
    global con
    try:
        con = fxcmpy.fxcmpy(config_file='config.cfg',
                            server='real')
    except:
        print('Connect fail, again')
        time.sleep(0.5)
        fxcmConnect()


def checkConnect():
    if con.is_connected() != True:
        con.close()
        print("FXCM disconnected")
        fxcmConnect()
        print("And FXCM disconnected")
        return {"status": "FXCM disconnected and disconnected"}
    else:
        print("FXCM Connected")
        return {"status": "FXCM Connected"}


def getRate(symbol):
    offersDF = con.get_offers()
    offersDF.set_index('currency', inplace=True)
    rate = offersDF.at[symbol, 'mmr']
    return rate


def calcAmount(total_order, symbol):
    accounts = con.get_accounts()
    usableMargin = accounts.at[0, 'usableMargin'] - \
        accounts.at[0, 'balance'] * 0.2
    try:
        openedPositions = con.get_open_positions().shape[0]
    except:
        openedPositions = 0
    if (total_order-openedPositions) > 0:
        amount = usableMargin/(total_order-openedPositions)/getRate(symbol)
        amount = math.floor(amount)
    else:
        amount = 0
    return amount


def fxcm(data):
    checkConnect()

    total_order = data['total_order']
    symbol = data['ticker'][:3]+"/"+data['ticker'][3:]
    side = True if data['side'] == 'buy' else False
    order_price = data['order_price']
    limit_price = data['limit_price']
    stop_price = data['stop_price']

    if data['side'] == 'close':
        # order = con.close_all_for_symbol(
        #     symbol=symbol, order_type='AtMarket', time_in_force='GTC')
        # msg = {'status': 'close_success'} if type(order) != type(None) else {
        #     'status': 'nothing to close'}
        msg = {'status': 'disabled force close'}
        return msg

    elif (data['side'] == 'buy' or data['side'] == 'sell'):
        amount = calcAmount(total_order, symbol)
        if amount >= 5:
            order = con.open_trade(symbol=symbol, is_buy=side,
                                   rate=order_price, limit=limit_price, stop=stop_price,
                                   amount=amount, time_in_force='GTC',
                                   order_type='AtMarket', is_in_pips=False)
            msg = {'status': 'order_success'} if type(order) != int else {
                'status': 'order_fail'}

        else:
            msg = {'status': 'fail_amount'}
    else:
        msg = {'status': 'empty_side'}
    return msg
