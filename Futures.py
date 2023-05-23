from main_zmq import signal_history_file_name, date_yesterday, date_today
import json
import os

QFF_MXF_202306 = {
    'future_A':'TC.F.TWF.QFF.202305',
    'future_B':'TC.F.TWF.MXF.202305',
    'future_A_Index': 100,
    'future_B_Index': 50,
    'ols_const': 351595.85,
    'ols_coef': 7,
    'opt_threshold': 800,
    'history_spread': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_buy_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_short_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_sell_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_cover_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
today_file_name = signal_history_file_name + date_today + "_latest"
yesterday_file_name = signal_history_file_name + date_yesterday + "_latest"
print(f"yesterday_file_name={yesterday_file_name}")
if os.path.isfile(f"{today_file_name}.txt"):
    with open(f"{today_file_name}.txt", "r") as f:
        QFF_MXF_202306 = json.load(f)
        print(f"load data: , {QFF_MXF_202306}")

elif os.path.isfile(f"{yesterday_file_name}.txt"):
    with open(f"{yesterday_file_name}.txt", "r") as f:
        QFF_MXF_202306 = json.load(f)
        print(f"load data: , {QFF_MXF_202306}")

QFF_TXF_202306 = {
    'future_A':'TC.F.TWF.QFF.202306',
    'future_B':'TC.F.TWF.TXF.202306',
    'future_A_Index': 100,
    'future_B_Index': 200,
    'ols_const': 1408153.46,
    'ols_coef': 31,
    'opt_threshold': 10900,
    'history_spread': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_buy_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_short_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_sell_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_cover_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

CDF_TXF_202306 = {
    'future_A':'TC.F.TWF.CDF.202306',
    'future_B':'TC.F.TWF.TXF.202306',
    'future_A_Index': 2000,
    'future_B_Index': 200,
    'ols_const': 1403332.62,
    'ols_coef': 1.58,
    'opt_threshold': 3500,
    'history_spread': [0],
    'history_buy_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_short_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_sell_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'history_cover_signal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}

CDF_Index = 2000
QFF_Index = 100
TXF_Index = 200
MXF_Index = 50

QFF_MXF_Threshold = 800
QFF_TXF_Threshold = 10900
CDF_TXF_Threshold = 3500
