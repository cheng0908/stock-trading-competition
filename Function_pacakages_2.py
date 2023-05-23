from tcoreapi_mq import *
import threading
from Function_packages import write_into_txt_file, orders_obj_generator, order_report
from Futures import *
from Trade_function import *
from main_zmq import date_today, position_data_file_name

futures = {}
quoteSymbol = None
quoteSymbol_2 = None
quoteSymbol_3 = None
quoteSymbol_4 = None
# stock_price_now = 0
strAccountMask = ""
arrInfo = None

count = 0


def future_new_order(g_TradeZMQ, g_TradeSession, symbol, arrInfo, price, order_qty, side, sleep_time, signal):
    time.sleep(sleep_time)
    order_obj = orders_obj_generator(symbol=symbol,
                                     arrInfo=arrInfo,
                                     price=price,
                                     time_in_force="2",
                                     side=side,
                                     order_type="1",
                                     order_qty=order_qty,
                                     position_effect="0")
    print(order_obj)
    s_order = g_TradeZMQ.NewOrder(g_TradeSession, order_obj)
    print(order_report(s_order))
    print(f"Order {symbol} successfully placed at {price}, side={side}, signal={signal}")


def trade_action(signal_dict, g_TradeZMQ, g_TradeSession, straddle_data):   # 要用futures price
    global arrInfo, futures
    # raise Exception("No trading now")

    for key in signal_dict:
        if key == "buy":    # sell c unit A and buy 1 unit B
            symbol_first = straddle_data['future_A']
            price_first = signal_dict['buy']['price']
            order_qty_first = straddle_data['ols_coef']
            side_first = 2
            sleep_time_first = 0
            t_trade = threading.Thread(target=future_new_order,
                                       args=(g_TradeZMQ, g_TradeSession, symbol_first,
                                             arrInfo, price_first, order_qty_first, side_first, sleep_time_first, key))
            t_trade.start()

            symbol_next = straddle_data['future_B']
            price_next = signal_dict['buy']['price']
            order_qty_next = 1
            side_next = 1
            sleep_time_next = 10
            t_trade_2 = threading.Thread(target=future_new_order,
                                       args=(g_TradeZMQ, g_TradeSession, symbol_next,
                                             arrInfo, price_next, order_qty_next, side_next, sleep_time_next, key))
            t_trade_2.start()

        elif key == "sell":     # sell 1 unit B, buy c unit A

            symbol_first = straddle_data['future_B']
            price_first = signal_dict['sell']['price']
            order_qty_first = 1
            side_first = 2
            sleep_time_first = 0
            t_trade = threading.Thread(target=future_new_order,
                                       args=(g_TradeZMQ, g_TradeSession, symbol_first,
                                             arrInfo, price_first, order_qty_first, side_first, sleep_time_first, key))
            t_trade.start()

            symbol_next = straddle_data['future_A']
            price_next = signal_dict['sell']['price']
            order_qty_next = straddle_data['ols_coef']
            side_next = 1
            sleep_time_next = 10
            t_trade_2 = threading.Thread(target=future_new_order,
                                         args=(g_TradeZMQ, g_TradeSession, symbol_next,
                                               arrInfo, price_next, order_qty_next, side_next, sleep_time_next, key))
            t_trade_2.start()


        elif key == "short":    # sell 1 unit B, buy c unit A

            symbol_first = straddle_data['future_B']
            price_first = signal_dict['short']['price']
            order_qty_first = 1
            side_first = 2
            sleep_time_first = 0
            t_trade = threading.Thread(target=future_new_order,
                                       args=(g_TradeZMQ, g_TradeSession, symbol_first,
                                             arrInfo, price_first, order_qty_first, side_first, sleep_time_first, key))
            t_trade.start()

            symbol_next = straddle_data['future_A']
            price_next = signal_dict['short']['price']
            order_qty_next = straddle_data['ols_coef']
            side_next = 1
            sleep_time_next = 10
            t_trade_2 = threading.Thread(target=future_new_order,
                                         args=(g_TradeZMQ, g_TradeSession, symbol_next,
                                               arrInfo, price_next, order_qty_next, side_next, sleep_time_next, key))
            t_trade_2.start()

        elif key == "cover":    # sell c unit A and buy 1 unit B
            symbol_first = straddle_data['future_A']
            price_first = signal_dict['cover']['price']
            order_qty_first = straddle_data['ols_coef']
            side_first = 2
            sleep_time_first = 0
            t_trade = threading.Thread(target=future_new_order,
                                       args=(g_TradeZMQ, g_TradeSession, symbol_first,
                                             arrInfo, price_first, order_qty_first, side_first, sleep_time_first, key))
            t_trade.start()

            symbol_next = straddle_data['future_B']
            price_next = signal_dict['cover']['price']
            order_qty_next = 1
            side_next = 1
            sleep_time_next = 10
            t_trade_2 = threading.Thread(target=future_new_order,
                                         args=(g_TradeZMQ, g_TradeSession, symbol_next,
                                               arrInfo, price_next, order_qty_next, side_next, sleep_time_next, key))
            t_trade_2.start()

        else:
            print("signal_dict_error")

    return "OK"


def update_futures_data(symbol, data):
    write_into_txt_file(filePath=f"{position_data_file_name}{date_today}.txt", data=data)
    return True


def CS_function(symbol, data, g_TradeZMQ, g_TradeSession):
    trade_price = '1'   #1 : Market order 2 : Limit order (LIMIT)
    trade_dict = {}

    global QFF_MXF_202306
    # quoteSymbol = "TC.F.TWF.QFF.202306" quoteSymbol_2 = "TC.F.TWF.MXF.202306"
    if symbol == quoteSymbol or symbol == quoteSymbol_2:
        if futures[QFF_MXF_202306['future_A']] != 0 and futures[QFF_MXF_202306['future_B']] != 0:
            signal = signal_pair_trade(future_A=QFF_MXF_202306['future_A'],
                                       future_B=QFF_MXF_202306['future_B'],
                                       point_A=QFF_MXF_202306['future_A_Index'],
                                       point_B=QFF_MXF_202306['future_B_Index'],
                                       prices_A=futures[QFF_MXF_202306['future_A']],
                                       price_B=futures[QFF_MXF_202306['future_B']],
                                       signal_history=QFF_MXF_202306,
                                       ols_const=QFF_MXF_202306['ols_const'],
                                       ols_coef=QFF_MXF_202306['ols_coef'],
                                       threshold=QFF_MXF_202306['opt_threshold'])
            QFF_MXF_202306 = signal_history_record(signal, QFF_MXF_202306)
            trade_result = identify_signal_status(signal_history=QFF_MXF_202306)
            if len(trade_result) != 0:
                for item in trade_result:
                    trade_dict[item] = {"price":trade_price}
                trade_action(signal_dict=trade_dict, g_TradeZMQ=g_TradeZMQ,
                             g_TradeSession=g_TradeSession, straddle_data=QFF_MXF_202306)
        else:
            print(f"future price is zero, {QFF_MXF_202306['future_A']}={futures[QFF_MXF_202306['future_A']]},"
                  f"{QFF_MXF_202306['future_B']}={futures[QFF_MXF_202306['future_B']]}")
    else:
        # trade_result = identify_signal_status(signal_history=QFF_MXF_202306)
        print("ERROR")

    return trade_dict


def create_futures_dict():
    global futures
    global quoteSymbol
    global quoteSymbol_2
    # global quoteSymbol_3
    # global quoteSymbol_4

    futures[quoteSymbol] = 0
    futures[quoteSymbol_2] = 0
    # futures[quoteSymbol_3] = 0
    # futures[quoteSymbol_4] = 0
    return "Futures dict is created"


def print_futures_price_now():
    global futures
    for keys, value in futures.items():
        print(f"{keys} = {value}")


def update_stock_price(symbol, price):
    global futures, count
    futures[symbol] = float(price)
    # update_futures_data(symbol="")
    # t_trade = threading.Thread(target=quote_sub_th, args=(g_QuoteZMQ, q_data["SubPort"], "", date_today))

    count += 1
    if count % 50 == 0:
        print_futures_price_now()
        count = 0


# 實時行情回補
def OnRealTimeQuote(symbol, file_name, g_TradeZMQ, g_TradeSession):
    if symbol["TradingPrice"] != '':
        # print(symbol)
        update_stock_price(symbol=symbol["Symbol"], price=symbol["TradingPrice"])
        update_futures_data(symbol=symbol["Symbol"], data=symbol)
        signal_dict= CS_function(symbol=symbol["Symbol"], data=symbol, g_TradeZMQ=g_TradeZMQ, g_TradeSession=g_TradeSession)
        # print("trade_action_return", trade_action(signal_dict=signal_dict, g_TradeZMQ=g_TradeZMQ, g_TradeSession=g_TradeSession, straddle_data=None))
        # write_into_txt_file(filePath=temp_text_file_name, data=symbol)
        # print("實時行情",symbol["HighPrice"])
    else:
        print(symbol)


# 實時Greeks回補
def OnGreeks(greek):
    print("實時Greeks", greek)


# 已登入資金帳號變更
def OnGetAccount(account):
    print(account["BrokerID"])


# 實時委託回報消息
# def OnexeReport(ReportID, report):
#     print("OnexeReport:", report["ReportID"])
#     ReportID = report["ReportID"]
#     return None
def OnexeReport(report):
    print("OnexeReport:", report["ReportID"])
    return None


# 實時成交回報回補
def RtnFillReport(report):
    print("RtnFillReport:", report["ReportID"])


# 查詢當日歷史委託回報回補
def ShowEXECUTIONREPORT(g_TradeZMQ, SessionKey, reportData):
    if reportData["Reply"] == "RESTOREREPORT":
        Orders = reportData["Orders"]
        if len(Orders) == 0:
            return
        last = ""
        for data in Orders:
            last = data
            print("查詢回報", data)
        reportData = g_TradeZMQ.QryReport(SessionKey, last["QryIndex"])
        ShowEXECUTIONREPORT(g_TradeZMQ, SessionKey, reportData)


# 查詢當日歷史委託成交回補
def ShowFillReport(g_TradeZMQ, SessionKey, reportData):
    if reportData["Reply"] == "RESTOREFILLREPORT":
        Orders = reportData["Orders"]
        if len(Orders) == 0:
            return

        last = ""
        for data in Orders:
            last = data
            print("查詢成交回報", data)
        reportData = g_TradeZMQ.QryFillReport(SessionKey, last["QryIndex"])
        ShowFillReport(g_TradeZMQ, SessionKey, reportData)


# 查詢部位消息回補
def ShowPOSITIONS(g_TradeZMQ, SessionKey, AccountMask, positionData):
    if positionData["Reply"] == "POSITIONS":
        position = positionData["Positions"]
        if len(position) == 0:
            return

        last = ""
        for data in position:
            last = data
            print("部位:" + data["Symbol"])

        positionData = g_TradeZMQ.QryPosition(SessionKey, AccountMask, last["QryIndex"])
        ShowPOSITIONS(g_TradeZMQ, SessionKey, AccountMask, positionData)


# 交易消息接收
def trade_sub_th(obj, sub_port, filter=""):
    socket_sub = obj.context.socket(zmq.SUB)
    # socket_sub.RCVTIMEO=5000           #ZMQ超時設定
    socket_sub.connect("tcp://127.0.0.1:%s" % sub_port)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, filter)
    while True:
        message = socket_sub.recv()
        if message:
            message = json.loads(message[:-1])
            # print("in trade message",message)
            if (message["DataType"] == "ACCOUNTS"):
                for i in message["Accounts"]:
                    OnGetAccount(i)
            elif (message["DataType"] == "EXECUTIONREPORT"):
                OnexeReport(message["Report"])
            elif (message["DataType"] == "FILLEDREPORT"):
                RtnFillReport(message["Report"])


# 行情消息接收
def quote_sub_th(obj, g_TradeZMQ, sub_port, g_TradeSession, filter="", file_name=""):
    socket_sub = obj.context.socket(zmq.SUB)
    # socket_sub.RCVTIMEO=7000   #ZMQ超時設定
    socket_sub.connect("tcp://127.0.0.1:%s" % sub_port)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, filter)
    while (True):
        message = (socket_sub.recv()[:-1]).decode("utf-8")
        index = re.search(":", message).span()[1]  # filter
        message = message[index:]
        message = json.loads(message)
        # for message in messages:
        if (message["DataType"] == "REALTIME"):
            OnRealTimeQuote(symbol=message["Quote"], file_name=file_name, g_TradeZMQ=g_TradeZMQ, g_TradeSession=g_TradeSession)
            # OnRealTimeQuote(message["Quote"], file_name, g_TradeZMQ, g_TradeSession)
        elif (message["DataType"] == "GREEKS"):
            OnGreeks(message["Quote"])
        elif (message["DataType"] == "TICKS" or message["DataType"] == "1K" or message["DataType"] == "DK"):
            # print("@@@@@@@@@@@@@@@@@@@@@@@",message)
            strQryIndex = ""
            while (True):
                s_history = obj.GetHistory(g_QuoteSession, message["Symbol"], message["DataType"], message["StartTime"],
                                           message["EndTime"], strQryIndex)
                historyData = s_history["HisData"]
                if len(historyData) == 0:
                    break

                last = ""
                for data in historyData:
                    last = data
                    print("歷史行情：Time:%s, Volume:%s, QryIndex:%s" % (data["Time"], data["Volume"], data["QryIndex"]))

                strQryIndex = last["QryIndex"]

    return


def login():
    # 登入
    g_TradeZMQ = TradeAPI("ZMQ", "8076c9867a372d2a9a814ae710c256e2")
    g_QuoteZMQ = QuoteAPI("ZMQ", "8076c9867a372d2a9a814ae710c256e2")

    t_data = g_TradeZMQ.Connect("51141")
    q_data = g_QuoteZMQ.Connect("51171")
    print(t_data)
    print(q_data)

    if q_data["Success"] != "OK":
        print("[quote]connection failed")
        return

    if t_data["Success"] != "OK":
        print("[trade]connection failed")
        return

    g_TradeSession = t_data["SessionKey"]
    g_QuoteSession = q_data["SessionKey"]

    return g_TradeZMQ, g_QuoteZMQ, g_TradeSession, g_QuoteSession, q_data, t_data


def logout(g_QuoteZMQ, g_TradeZMQ, g_QuoteSession, g_TradeSession):
    # 登出
    q_logout = g_QuoteZMQ.Logout(g_QuoteSession)
    print(q_logout)
    t_logout = g_TradeZMQ.Logout(g_TradeSession)
    print(t_logout)


def check_specific_order(g_QuoteZMQ, g_QuoteSession, symbol, type="Future"):
    # 查詢指定合约訊息
    print("查詢指定合約：", g_QuoteZMQ.QueryInstrumentInfo(g_QuoteSession, symbol))
    # 查詢指定類型合約列表
    # 期貨：Future
    # 期權：Options
    # 證券：Stock
    print("查詢合約：", g_QuoteZMQ.QueryAllInstrumentInfo(g_QuoteSession, type))


def query_trade_acc_info(g_TradeZMQ, g_TradeSession):  # 查詢已登入資金帳號
    global strAccountMask, arrInfo

    accountInfo = g_TradeZMQ.QryAccount(g_TradeSession)
    if accountInfo != None:
        arrInfo = accountInfo["Accounts"]
        if len(arrInfo) != 0:
            # print("@@@@@@@@@@@:",arrInfo[0],"\n")
            strAccountMask = arrInfo[0]["AccountMask"]


def query_entrustment_records(g_TradeZMQ, g_TradeSession):  # 查詢委託紀錄
    reportData = g_TradeZMQ.QryReport(g_TradeSession, "")
    ShowEXECUTIONREPORT(g_TradeZMQ=g_TradeZMQ, SessionKey=g_TradeSession, reportData=reportData)
    fillReportData = g_TradeZMQ.QryFillReport(g_TradeSession, "")
    ShowFillReport(g_TradeZMQ=g_TradeZMQ, SessionKey=g_TradeSession, reportData=fillReportData)


def query_funds(g_TradeZMQ, g_TradeSession):  # 查詢資金
    global strAccountMask

    if strAccountMask != "":
        print(g_TradeZMQ.QryMargin(g_TradeSession, strAccountMask))


def query_position(g_TradeZMQ, g_TradeSession):  # 查詢持倉
    global strAccountMask

    positionData = g_TradeZMQ.QryPosition(g_TradeSession, strAccountMask, "")
    ShowPOSITIONS(g_TradeZMQ=g_TradeZMQ, SessionKey=g_TradeSession, AccountMask=strAccountMask,
                  positionData=positionData)

# #實時行情訂閱
# #解除訂閱
# g_QuoteZMQ.UnsubQuote(g_QuoteSession,"TC.F.TWF.FITX.HOT")
# #訂閱實時行情
# g_QuoteZMQ.SubQuote(g_QuoteSession,"TC.F.TWF.FITX.HOT")
#
# #實時Greeks訂閱
# #解除訂閱
# g_QuoteZMQ.UnsubGreeks(g_QuoteSession,"TC.F.TWF.FITX.HOT")
# #訂閱實時行情
# g_QuoteZMQ.SubGreeks(g_QuoteSession,"TC.F.TWF.FITX.HOT")
#
# #訂閱歷史數據
# g_QuoteZMQ.SubHistory(g_QuoteSession, "TC.F.TWF.FITX.HOT", "1K", "2020113000", "2020120100")
