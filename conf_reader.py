import csv,os
from classes import STOCK
import logging

import logging, os, configparser

logger = logging.getLogger("IndiBotLog")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('IndiBot.log', 'w+')
fh.setFormatter(formatter)
fh.setLevel(logging.INFO)
logger.addHandler(fh)

log = logging.getLogger("IndiBotLog")

#Read credentials from config.ini
configParser = configparser.ConfigParser()
configParser.read("config_rename.ini")
props = dict(configParser.items("DEFAULT"))


# MYDEF = []
# ALLSTOCKS = []
#
# print(os.getcwd())
#
# with open('data1.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     stock_req_code = 2000
#     for row in csv_reader:
#         if line_count == 0:
#             # print(f'Column names are {", ".join(row)}')
#             # log.info("Column names are {", ".join(row)}")
#             line_count += 1
#         else:
#             stock = STOCK.STOCK()
#             stock.symbol = row[1]
#             ALLSTOCKS.append(stock.symbol)
#             stock.buy_or_sell = row[2]
#             stock.quantity = row[3]
#             stock.profit_price_gap_perc = row[4]
#             stock.margin_price = row[5]
#             stock.stop_loss_per = row[6]
#             stock.req_code = stock_req_code
#             stock_req_code += 1
#             if row[4].capitalize() == "yes".capitalize():
#                 MYDEF.append(stock)
#                 line_count += 1
#                 print_str = "Stock: {} | Buy/Sell: {} | Quantity: {} | Price Gap %: {} | Margin Price: {} | Request Code: {}".format(stock.symbol,
#                                                                                                                                      stock.quantity,
#                                                                                                                                      stock.buy_or_sell,
#                                                                                                                                      stock.profit_price_gap_perc,
#                                                                                                                                      stock.margin_price,
#                                                                                                                                      stock.req_code)
#                 print(print_str)
#                 log.info(print_str)
#     print(f'Total  {line_count - 1} stocks found in data.csv.')
#     log.info("Total {} stocks found in data.csv".format(line_count - 1))
