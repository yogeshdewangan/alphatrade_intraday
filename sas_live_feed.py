from alphatrade import AlphaTrade, LiveFeedType
import conf_reader,time
import stock_data
from classes.StockOpen import StockOpen

login_id = conf_reader.props["alpha_login_id"]
password = conf_reader.props["alpha_password"]
twofa = conf_reader.props["alpha_twofa"]

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None

sas = AlphaTrade(login_id=login_id, password=password,
                 twofa=twofa, access_token=access_token, master_contracts_to_download=['NSE'])

socket_opened = False

stock_current_price_dic ={}

stock_open_list = {}

def event_handler_quote_update(message):
    global stock_current_price_dic
    global stock_open_list
    ltp = message['ltp']
    symbol = str(message['instrument']).split("symbol='")[1].split("'")[0]
    stock_current_price_dic[symbol] = ltp
    stock_open_list[symbol] = str(message['open']) + ',' + str(message['high']) + ',' + str(message['low'])+ ',' + str(message['ltp'])
    pass
    # print(stock_open_list)
    # print(f'ticks :: {message}')


def open_callback():
    global socket_opened
    socket_opened = True


sas.start_websocket(subscribe_callback=event_handler_quote_update,
                    socket_open_callback=open_callback,
                    run_in_background=True)
while (socket_opened == False):
    pass


for stock in stock_data.MYDEF:
    instrument = sas.get_instrument_by_symbol('NSE', stock.symbol)
    sas.subscribe(instrument, LiveFeedType.MARKET_DATA)
time.sleep(10)

