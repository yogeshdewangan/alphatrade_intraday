# import conf_reader
# import traceback
# import time, random, logging
# from datetime import datetime
# import symbol_price
#
# # # Enable below to trade with fyers
# # from classes import bridge as bridge
# # broker_name = "Fyers"
#
# # Enable below to trade with sas onlne alpha
# import stock_data
# from classes import alpha as bridge
# broker_name = "SAS Online"
#
#
# log = logging.getLogger("IndiBotLog")
#
# import os
# import shutil
#
# for root, dirs, files in os.walk('stock_data'):
#     try:
#         for f in files:
#             os.unlink(os.path.join(root, f))
#         for d in dirs:
#             shutil.rmtree(os.path.join(root, d))
#     except:
#         pass
#
#
# def get_price_range(price, margin_price):
#     variation_amount = margin_price
#     price = float(price)
#     return price + variation_amount, price - variation_amount
#
#
# def calculate_percentage(price, percentage, margin_price):
#     price = float(price)
#     percentage = float(percentage)
#     margin_price = float(margin_price)
#     p1, p2 = get_price_range(price + (price * (percentage / 100)), margin_price)
#     n1, n2 = get_price_range(price - (price * (percentage / 100)), margin_price)
#     return round(p1, 2), round(p2, 2), round(n1, 2), round(n2, 2)
#
#
# def log_stock(symbol, data):
#     try:
#         with open("stock_data/" + symbol + ".txt", "a") as f:
#             f.write(str(datetime.now()) + " - " + data +"\n")
#     except:
#         pass
#
#
# def word_count(str):
#     counts = dict()
#     words = str.split()
#
#     for word in words:
#         if word in counts:
#             counts[word] += 1
#         else:
#             counts[word] = 1
#
#     return counts
#
#
# def stop_loss_per_calculate(current_price, per, buy_or_sell):
#     per = float(per)
#     current_price = float(current_price)
#     if per ==0.0:
#         if broker_name == "Fyers":
#             return 0
#         else:
#             return None
#     if buy_or_sell.upper() == "buy".upper():
#         stop_loss = current_price - (current_price * (per / 100))
#     else:
#         stop_loss = current_price + (current_price * (per / 100))
#     return round(stop_loss,2)
#
#
# if __name__ == '__main__':
#     print("******** Broker : " + broker_name + " *********")
#
#     first_time = False
#     while True:
#
#         stocks_to_trade = symbol_price.get_list_of_stocks_to_trade()
#
#         stop_list = []
#         try:
#             with open('stop.txt') as f:
#                 stop_list = f.read().splitlines()
#         except:
#             pass
#
#         if not first_time:
#             for stock in stocks_to_trade:
#                 if not stock.symbol in stop_list:
#                     try:
#                         current_price = symbol_price.get_current_price(stock.symbol)
#                         stop_loss = stop_loss_per_calculate(current_price, stock.stop_loss_per, stock.buy_or_sell)
#                         is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=stock.quantity, buy_or_sell=stock.buy_or_sell,
#                                                           current_price=current_price, stop_loss=stop_loss)
#                         if is_placed:
#                             print("Current price: {}".format(current_price))
#                             print_str = "[First Order] " + stock.symbol + " " + stock.buy_or_sell.capitalize() + " - price: " + str(
#                                 current_price) + " quantity: " + str(stock.quantity) + " Stop Loss: " +str(stop_loss)
#                             stock.order += stock.buy_or_sell.capitalize() + " "
#                             log.info(print_str)
#                             print(print_str)
#                             stock.ltp = current_price
#                             log_stock(stock.symbol, print_str)
#
#                     except Exception as e:
#                         log.info("Exception while placing first order for symbol: {} Exception: {}".format(stock.symbol, traceback.print_exc()))
#                         print("Exception while placing first order for symbol: {}  Exception: {}".format(stock.symbol, traceback.print_exc()))
#                 else:
#                     print("Stock found in stop list: {}".format(stock.symbol))
#                 print("==================================================================")
#                 print("==================================================================")
#             first_time = True
#
#         for stock in conf_reader.MYDEF:
#             if not stock.symbol in stop_list:
#                 try:
#                     current_price = symbol_price.get_current_price(stock.symbol)
#
#                     pos_value_var1, pos_value_var2, neg_value_var1, neg_value_var2 = calculate_percentage(stock.ltp, stock.profit_price_gap_perc,
#                                                                                                           stock.margin_price)
#
#                     print("{} LTP: {}".format(stock.symbol, stock.ltp))
#                     print("{} Current Price: {}".format(stock.symbol, current_price))
#
#                     print("Positive Var1: {}".format(pos_value_var1))
#                     print("Positive Var2: {}".format(pos_value_var2))
#                     print("Negative Var1: {}".format(neg_value_var1))
#                     print("Negative Var2: {}".format(neg_value_var2))
#
#                     if current_price <= pos_value_var1 and current_price >= pos_value_var2:
#                         stop_loss = stop_loss_per_calculate(current_price, stock.stop_loss_per, stock.buy_or_sell)
#                         is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=int(stock.quantity), buy_or_sell="sell", current_price=current_price,
#                                                           stop_loss=stop_loss)
#                         if is_placed:
#                             print_str = "Positive Var1: {} | Positive Var2: {} | Negative Var1: {} | Negative Var2: {}".format(str(pos_value_var1),
#                                                                                                                                str(pos_value_var2),
#                                                                                                                                str(neg_value_var1),
#                                                                                                                                str(neg_value_var2))
#                             print(print_str)
#                             log.info(print_str)
#                             print_str = stock.symbol + " SELL - price: " + str(current_price) + " quantity: " + str(
#                                 int(stock.quantity)) + " Stop Loss: " + str(stop_loss)
#                             stock.order += "Sell "
#                             log.info(print_str)
#                             stock.ltp = current_price
#                             log_stock(stock.symbol, print_str)
#
#                     if current_price <= neg_value_var1 and current_price >= neg_value_var2:
#                         stop_loss = stop_loss_per_calculate(current_price, stock.stop_loss_per, stock.buy_or_sell)
#                         is_placed = bridge.purchase_stock(symbol=stock.symbol, quantity=int(stock.quantity), buy_or_sell="buy", current_price=current_price,
#                                                           stop_loss=stop_loss)
#                         if is_placed:
#                             print_str = "Positive Var1: {} | Positive Var2: {} | Negative Var1: {} | Negative Var2: {}".format(str(pos_value_var1),
#                                                                                                                                str(pos_value_var2),
#                                                                                                                                str(neg_value_var1),
#                                                                                                                                str(neg_value_var2))
#                             print(print_str)
#                             log.info(print_str)
#                             print_str = stock.symbol + " BUY - price: " + str(current_price) + " quantity: " + str(
#                                 int(stock.quantity)) + " Stop Loss: " + str(stop_loss)
#                             stock.order += "Buy "
#                             log.info(print_str)
#                             stock.ltp = current_price
#                             log_stock(stock.symbol, print_str)
#
#                 except Exception:
#                     log.info("Exception: {}".format(traceback.print_exc()))
#                     print("Exception: {}".format(traceback.print_exc()))
#                 print(stock.symbol + " - " + stock.order)
#                 log.info(stock.symbol + " - " + stock.order)
#                 print("Buy/Sell count: " + str(word_count(stock.order)))
#             else:
#                 print("Stock found in stop list: {}".format(stock.symbol))
#             print("==================================================================")
#             print("==================================================================")
#         wait_time = 5
#         print("Wating for {} seconds".format(wait_time))
#         time.sleep(wait_time)
