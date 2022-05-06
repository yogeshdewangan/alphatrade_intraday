# Real Time Data Sample - Using TrueData Websocket Python Library

from truedata_ws.websocket.TD import TD
from copy import deepcopy
import time, json
from datetime import datetime
import conf_reader


username = conf_reader.props["truedata_userid"]
password = conf_reader.props["truedata_password"]

# Default ports are 8082 / 8092 in the library
realtime_port = 8082
history_port = 8092

td_app = TD(username, password, live_port=realtime_port, historical_port=history_port)

symbols = conf_reader.ALLSTOCKS
req_ids = td_app.start_live_data(symbols)
time.sleep(2)


def get_current_data(stock_code):
    live_data_objs = {}
    for req_id in req_ids:
        live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])

    data = str(live_data_objs[stock_code])
    json_data = json.loads(data.split("ltp': ")[1].split(",")[0])
    return json_data

def get_historic_data():
    hist_data_1 = td_app.get_historic_data("ITC", bar_size="15 min", start_time=datetime(2021, 2, 5, 9, 30),end_time=datetime(2021, 2, 5, 9, 45))  # remove duration for current date
    high= hist_data_1[0]["h"]
    low = hist_data_1[0]["l"]
    return high, low








