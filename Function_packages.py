import logging

logging.basicConfig(format="%(asctime)-15s %(message)s", filename="program_log.log", level=logging.WARNING)     #Debug, Info, Warning, Error, Critical



def write_into_txt_file(filePath="temp.txt", data=None):
    if data != None:
        # f = open(filePath,'a',encoding='utf8')
        # f.write(str(data))
        # f.write('\n')
        # f.close()
        with open(filePath, 'a', encoding='utf8') as f:
            f.write(str(data))
            f.write('\n')


def orders_obj_generator(symbol=None, arrInfo=None, price=None, time_in_force=1, side=1, order_type=1,
                         order_qty=None, position_effect=0):

    if symbol == None or arrInfo == None or price == None or order_qty == None:
        logging.warning([symbol, arrInfo, price, time_in_force, side, order_type, order_qty, position_effect])
        orders_obj = None
    else:
        orders_obj = {
            "Symbol": f"{symbol}",
            "BrokerID": arrInfo[0]['BrokerID'],
            "Account": arrInfo[0]['Account'],
            "Price": f"{price}",
            "TimeInForce": f"{time_in_force}",
            "Side": f"{side}",
            "OrderType": f"{order_type}",  # 1 : Market order 2 : Limit order (LIMIT)
            "OrderQty": f"{order_qty}",
            "PositionEffect": f"{position_effect}"
        }

    return orders_obj


def order_report(s_order):
    message = None
    if s_order['Success'] == "OK":
        message = "下單成功"
    elif s_order['ErrCode'] == "-10":
        message = "unknow error"
    elif s_order['ErrCode'] == "-11":
        message = "買賣別錯誤"
    elif s_order['ErrCode'] == "-12":
        message = "複式單商品代碼解析錯誤 "
    elif s_order['ErrCode'] == "-13":
        message = "下單帳號,不可下此交易所商品"
    elif s_order['ErrCode'] == "-14":
        message = "下單錯誤,不支持的 價格 或 OrderType 或 TimeInForce"
    elif s_order['ErrCode'] == "-15":
        message = "不支援證券下單"
    elif s_order['ErrCode'] == "-20":
        message = "未建立連線"
    elif s_order['ErrCode'] == "-22":
        message = "價格的 TickSize 錯誤"
    elif s_order['ErrCode'] == "-23":
        message = "下單數量超過該商品的上下限 "
    elif s_order['ErrCode'] == "-24":
        message = "下單數量錯誤 "
    elif s_order['ErrCode'] == "-25":
        message = "價格不能小於和等於 0 (市價類型不會去檢查）"

    return message