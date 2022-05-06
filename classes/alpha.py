

from alphatrade import AlphaTrade
from alphatrade import TransactionType
from alphatrade import OrderType
from alphatrade import ProductType
import conf_reader
import enum, json


login_id = conf_reader.props["alpha_login_id"]
password = conf_reader.props["alpha_password"]
twofa = conf_reader.props["alpha_twofa"]


class OrderType(enum.Enum):
    Market = 'MARKET'
    Limit = 'LIMIT'
    StopLossLimit = 'SL'
    StopLossMarket = 'SL-M'

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None
sas = AlphaTrade(login_id=login_id, password=password, twofa=twofa)

sas = AlphaTrade(login_id=login_id, password=password,
                 twofa=twofa, access_token=access_token, master_contracts_to_download=['NSE'])



def get_balance():
    try:
        balance = sas.get_balance()
        print("Unrealized M2M: "+ str(balance["data"]["cash_positions"][0]["utilized"]["unrealised_m2m"]))
        print("Realized M2M: " + str(balance["data"]["cash_positions"][0]["utilized"]["realised_m2m"]))
        print("M2M: "+ str(sas.get_total_m2m()))
    except:
        pass



def purchase_stock(symbol, quantity, buy_or_sell="buy", current_price=0, stop_loss=None):

    if buy_or_sell.upper() == "buy".upper():
        TransType = TransactionType.Buy
    else:
        TransType = TransactionType.Sell

    if stop_loss is None:
        order_type = OrderType.Market
        product_type = ProductType.Intraday
    else:
        order_type = OrderType.Market
        product_type = ProductType.CoverOrder

    res = sas.place_order(transaction_type = TransType,
                         instrument = sas.get_instrument_by_symbol('NSE', symbol),
                         quantity = int(quantity),
                         order_type = order_type,
                         product_type = product_type,
                         price = 0.0,
                         trigger_price = stop_loss,
                         stop_loss = None,
                         square_off = None,
                         trailing_sl = None,
                         is_amo = False)
    if res["status"] == "success":
        order_id = res["data"]["oms_order_id"]
        order_history =  sas.get_order_history(order_id)
        status = order_history["data"][0]["order_status"]
        if status == "rejected":
            print_str = "Failed to place order for : Symbol: {} | Quantity: {} | Type: {} | at Price: {} | Stop Loss: {}".format(symbol, quantity, buy_or_sell, current_price, stop_loss)
            print(print_str)
            return False
        print_str = "Order Details : Symbol: {} | Quantity: {} | Type: {} | at Price: {} | Stop Loss: {}".format(symbol, quantity, buy_or_sell, current_price, stop_loss)
        print(print_str)
        get_balance()
        return True
    else:
        print_str = "Failed to place order for: Symbol: {} | Quantity: {} | Type: {} | at Price: {} | Stop Loss: {}".format(symbol, quantity, buy_or_sell, current_price, stop_loss)
        print(print_str)
        print(res["message"])
        return False

