import time
from tcoreapi_mq import * 
import tcoreapi_mq
import threading
from Function_packages import *
import Function_pacakages_2
from Function_pacakages_2 import *
from datetime import datetime, timedelta


g_TradeZMQ = None
g_QuoteZMQ = None
g_TradeSession = ""
g_QuoteSession = ""
ReportID=""
date_today = str(datetime.now().strftime("%Y_%m_%d"))
date_yesterday = datetime.now() - timedelta(days=1)
date_yesterday = str(date_yesterday.strftime("%Y_%m_%d"))
signal_history_file_name = "signal_history_"
position_data_file_name= "position_data_"


def main():

    global g_TradeZMQ
    global g_QuoteZMQ
    global g_TradeSession
    global g_QuoteSession
    global q_data
    global t_data
    global date_today
    #最後鎖定小台指跟小台積電
    # quoteSymbol = "TC.F.TWF.FITX.HOT"
    Function_pacakages_2.quoteSymbol = "TC.F.TWF.QFF.202305"    #小台積電 OK
    Function_pacakages_2.quoteSymbol_2 = "TC.F.TWF.MXF.202305"  #小台指 OK
    # quoteSymbol_3 = "TC.F.TWF.FIMT4.202304"
    # Function_pacakages_2.quoteSymbol_3 = "TC.F.TWF.CDF.202306"   #台積電 OK
    # Function_pacakages_2.quoteSymbol_4 = "TC.F.TWF.TXF.202306"  #台指 OK
    print(create_futures_dict())

    g_TradeZMQ, g_QuoteZMQ, g_TradeSession, g_QuoteSession, q_data, t_data = login()

#######################################################################交易##################################################
    # #建立一個交易線程
    t1 = threading.Thread(target=trade_sub_th, args=(g_TradeZMQ, t_data["SubPort"],))
    t1.start()

    query_trade_acc_info(g_TradeZMQ, g_TradeSession)
    if Function_pacakages_2.strAccountMask != "":
        print("Query:\n")
        query_entrustment_records(g_TradeZMQ, g_TradeSession)
        query_funds(g_TradeZMQ, g_TradeSession)
        query_position(g_TradeZMQ, g_TradeSession)

    #
    #         #改單
    #         reporders_obj={
    #             "ReportID":"142733892F",
    #             "ReplaceExecType":"0",
    #             "Price":"0.021"
    #             }
    #         reorder=g_TradeZMQ.ReplaceOrder(g_TradeSession,reporders_obj)
    #
    #         #刪單
    #         print("%%%%%%%%%%%%%%%%%%%%%%%%%",reorder)
    #         canorders_obj={
    #             "ReportID":"142921137H",
    #             }
    #         canorder=g_TradeZMQ.CancelOrder(g_TradeSession,canorders_obj)
    #         print("%%%%%%%%%%%%%%%%%%%%%%%%%",canorder)

#####################################################################行情################################################
    #建立一個行情線程
    t2 = threading.Thread(target = quote_sub_th,args=(g_QuoteZMQ, g_TradeZMQ, q_data["SubPort"], g_TradeSession, "", date_today))
    t2.start()

    g_QuoteZMQ.SubQuote(g_QuoteSession, Function_pacakages_2.quoteSymbol)
    g_QuoteZMQ.SubQuote(g_QuoteSession, Function_pacakages_2.quoteSymbol_2)
    # g_QuoteZMQ.SubQuote(g_QuoteSession, Function_pacakages_2.quoteSymbol_3)
    # g_QuoteZMQ.SubQuote(g_QuoteSession, Function_pacakages_2.quoteSymbol_4)

    # while True:
    #     time.sleep(15)
    #     print("main=", stock_price_now)




if __name__ == '__main__':
    main()