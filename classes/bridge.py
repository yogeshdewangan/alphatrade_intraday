"""
type*	int	1 => Limit Order
2 => Market Order
3 => Stop Order (SL-M)
4 => Stoplimit Order (SL-L)
side*	int	1 => Buy
-1 => Sell
"""

"""
CNC => For equity only
INTRADAY => Applicable for all segments.
MARGIN => Applicable only for derivatives
CO => Cover Order
BO => Bracket Order
"""

import conf_reader
from classes import fyers_auth
from fyers_api import fyersModel
import json, logging

log = logging.getLogger("IndiBotLog")

fyers = fyersModel.FyersModel()


def purchase_stock(symbol, quantity, buy_or_sell="buy", current_price=0, stop_loss=0):
    if buy_or_sell == "buy":
        side = 1
    else:
        side = -1
    quantity = int(quantity)

    if stop_loss > 0:
        product_type = "CO"
    else:
        product_type = "INTRADAY"

    res = fyers.place_orders(
        token=fyers_auth.access_token,
        data={
            "symbol": "NSE:" + symbol + "-EQ",
            "qty": quantity,
            "type": 2,
            "side": side,
            "productType": product_type,
            "limitPrice": 0,
            "stopPrice": 0,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": "False",
            "stopLoss": stop_loss,
            "takeProfit": 0
        }
    )
    if res["code"] == 200:
        print_str = "Order Details : Symbol: {} | Quantity: {} | Type: {} | at Price: {} | Stop Loss: {}".format(symbol, quantity, buy_or_sell, current_price,
                                                                                                                 stop_loss)
        print(print_str)
        log.info(print_str)
        return True
    else:
        print_str = "Failed to place order for: Symbol: {} | Quantity: {} | Type: {} | at Price: {} | Stop Loss: {}".format(symbol, quantity, buy_or_sell,
                                                                                                                            current_price, stop_loss)
        print(print_str)
        log.info(print_str)
        print(res["message"])
        log.info(res["message"])
        return False


def exit_position(symbol, id):
    response = fyers.exit_positions(
        token=fyers_auth.access_token,
        data={
            "id": id
        }
    )

    if response["code"] == 200:
        print("Position closed for: " + symbol)
        log.info("Position closed for: " + symbol)
        return True
    return False


def get_position(symbol):
    response = fyers.positions(fyers_auth.access_token)
    # f = open('dummy_positions.json', "r")
    # response = json.load(f)
    # f.close()
    stock_position = ""
    if response["code"] == 200:
        net_positions = response["data"]["netPositions"]
        for position in net_positions:
            if symbol in position["symbol"]:
                stock_position = position
                break

    return stock_position
