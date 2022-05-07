import traceback
import time, logging
from datetime import datetime
import symbol_price

# # Enable below to trade with fyers
# from classes import bridge as bridge
# broker_name = "Fyers"

# Enable below to trade with sas onlne alpha
import stock_data
from classes import alpha as bridge

broker_name = "SAS Online"

log = logging.getLogger("IndiBotLog")

import os
import shutil

for root, dirs, files in os.walk('stock_data'):
    try:
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    except:
        pass


def get_price_range(price, margin_price):
    variation_amount = margin_price
    price = float(price)
    return price + variation_amount


def calculate_target_price(current_price, per, buy_or_sell):
    per = float(per)
    current_price = float(current_price)

    if buy_or_sell.upper() == "sell".upper():
        stop_loss = current_price - (current_price * (per / 100))
    else:
        stop_loss = current_price + (current_price * (per / 100))
    return __round_nearest(round(stop_loss, 2))


def log_stock(symbol, data):
    try:
        with open("stock_data/" + symbol + ".txt", "a") as f:
            f.write(str(datetime.now()) + " - " + data + "\n")
    except:
        pass


def word_count(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def __round_nearest(x, a=0.05):
    return round((round(x / a) * a), 2)


def calculate_stop_loss(current_price, per, buy_or_sell):
    per = float(per)
    current_price = float(current_price)

    if buy_or_sell.upper() == "buy".upper():
        stop_loss = current_price - (current_price * (per / 100))
    else:
        stop_loss = current_price + (current_price * (per / 100))
    return __round_nearest(round(stop_loss, 2))


if __name__ == '__main__':
    print("******** Broker : " + broker_name + " *********")

    first_time = False
    stocks_to_trade = symbol_price.get_list_of_stocks_to_trade()
    while True:

        stop_list = []
        try:
            with open('stop.txt') as f:
                stop_list = f.read().splitlines()
        except:
            pass

        if not first_time:
            for stock in stocks_to_trade:
                if not stock.symbol in stop_list:
                    try:
                        current_price = symbol_price.get_current_price(stock.symbol)

                        is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=stock.quantity,
                                                          buy_or_sell=stock.buy_or_sell,
                                                          current_price=current_price)
                        if is_placed:
                            print("Current price: {}".format(current_price))
                            print_str = "[First Order] " + stock.symbol + " " + stock.buy_or_sell.capitalize() + " - price: " + str(
                                current_price) + " quantity: " + str(stock.quantity)
                            stock.trade_on = True
                            log.info(print_str)

                            print(print_str)
                            log_stock(stock.symbol, print_str)

                    except Exception as e:
                        log.info("Exception while placing first order for symbol: {} Exception: {}".format(stock.symbol,
                                                                                                           traceback.print_exc()))
                        print("Exception while placing first order for symbol: {}  Exception: {}".format(stock.symbol,
                                                                                                         traceback.print_exc()))
                else:
                    print("Stock found in stop list: {}".format(stock.symbol))
                print("==================================================================")
                print("==================================================================")
            first_time = True

        for stock in stocks_to_trade:
            if not stock.symbol in stop_list:
                try:
                    current_price = symbol_price.get_current_price(stock.symbol)

                    print("{} LTP: {}".format(stock.symbol, stock.ltp))
                    print("{} Current Price: {}".format(stock.symbol, current_price))

                    target_price = calculate_target_price(current_price, stock.profit_per, stock.buy_or_sell)
                    stop_loss = calculate_stop_loss(current_price, stock.stop_loss_per, stock.buy_or_sell)

                    if stock.buy_or_sell == "buy" and stock.trade_on == True:
                        if current_price >= target_price or current_price <= stop_loss:
                            is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=int(stock.quantity),
                                                              buy_or_sell="sell", current_price=current_price,
                                                              stop_loss=stop_loss)
                            if is_placed:
                                print_str = stock.symbol + " SELL - price: " + str(current_price) + " quantity: " + str(
                                    int(stock.quantity)) + " Stop Loss: " + str(stop_loss)
                                stock.trade_on == False
                                log.info(print_str)
                                log_stock(stock.symbol, print_str)
                                print(print_str)

                    if stock.buy_or_sell == "sell" and stock.trade_on == True:
                        if current_price <= target_price or current_price >= stop_loss:
                            is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=int(stock.quantity),
                                                              buy_or_sell="buy", current_price=current_price,
                                                              stop_loss=stop_loss)
                            if is_placed:
                                print_str = stock.symbol + " BUY - price: " + str(current_price) + " quantity: " + str(
                                    int(stock.quantity)) + " Stop Loss: " + str(stop_loss)
                                stock.trade_on == False
                                log.info(print_str)
                                log_stock(stock.symbol, print_str)
                                print(print_str)

                except Exception:
                    log.info("Exception: {}".format(traceback.print_exc()))
                    print("Exception: {}".format(traceback.print_exc()))
            else:
                print("Stock found in stop list: {}".format(stock.symbol))
            print("==================================================================")
            print("==================================================================")
        wait_time = 5
        print("Wating for {} seconds".format(wait_time))
        time.sleep(wait_time)
