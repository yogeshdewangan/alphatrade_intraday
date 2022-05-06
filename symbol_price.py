import conf_reader

import sas_live_feed
from classes.STOCK import STOCK
import stock_data

stop_loss_per = conf_reader.props["stop_loss_per"]
profit_per = conf_reader.props["profit_per"]

def get_current_price(symbol):
    return sas_live_feed.stock_current_price_dic[symbol]


def get_list_of_stocks_to_trade():
    stocks_to_trade = []
    for symbol in sas_live_feed.stock_open_list:
        stock = STOCK()
        symbol_data =  sas_live_feed.stock_open_list[symbol]
        temp = symbol_data.split(",")
        open= float(temp[0])
        high= float(temp[1])
        low= float(temp[2])
        ltp= float(temp[3])
        if open == high and ltp < 1000:
            stock.buy_or_sell = "sell"
            stock.symbol = symbol
            stock.open = float(open)
            stock.high = float(high)
            stock.low = float(low)
            stock.ltp = float(ltp)
            stock.stop_loss_per = int(stop_loss_per)
            stock.profit_per = int(profit_per)
            stocks_to_trade.append(stock)
        if open == low and ltp < 1000:
            stock.buy_or_sell = "buy"
            stock.symbol = symbol
            stock.open = float(open)
            stock.high = float(high)
            stock.low = float(low)
            stock.ltp = float(ltp)
            stock.stop_loss_per = int(stop_loss_per)
            stock.profit_per = int(profit_per)
            stocks_to_trade.append(stock)
    for stock in stocks_to_trade:
        for stock_mydef in stock_data.MYDEF:
            if stock.symbol == stock_mydef.symbol:
                stock.quantity = stock_mydef.quantity
    print("Found {} stocks to be traded".format( len(stocks_to_trade)))
    return stocks_to_trade




