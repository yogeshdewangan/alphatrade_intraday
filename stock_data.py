import csv, logging
from classes import STOCK

log = logging.getLogger("IndiBotLog")

MYDEF = []
ALLSTOCKS = []

with open('data1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    stock_req_code = 2000
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            # log.info("Column names are {", ".join(row)}")
            line_count += 1
        else:
            stock = STOCK.STOCK()
            stock.symbol = row[1]
            ALLSTOCKS.append(stock.symbol)
            stock.buy_or_sell = row[2]
            stock.quantity = row[3]
            stock.req_code = stock_req_code
            stock_req_code += 1
            if row[4].capitalize() == "yes".capitalize():
                MYDEF.append(stock)
                line_count += 1
                # print_str = "Stock: {} | Buy/Sell: {} | Quantity: {} ".format(stock.symbol, stock.buy_or_sell,
                #                                                               stock.quantity)
                # print(print_str)
                # log.info(print_str)
    print(f'Total  {line_count - 1} stocks found in data.csv.')
    log.info("Total {} stocks found in data.csv".format(line_count - 1))
