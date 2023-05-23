import time
import json
from main_zmq import date_today, signal_history_file_name, date_yesterday

count = 0
# price_B = s_0 - c * prices_A

def identify_signal_status(signal_history):
    return_signal = []
    if signal_history['history_buy_signal'][-2] == 0 and signal_history['history_buy_signal'][-1] == 1:
        return_signal.append('buy')

    if signal_history['history_short_signal'][-2] == 0 and signal_history['history_short_signal'][-1] == 1:
        return_signal.append('short')

    if signal_history['history_sell_signal'][-2] == 0 and signal_history['history_sell_signal'][-1] == 1:
        return_signal.append('sell')

    if signal_history['history_cover_signal'][-2] == 0 and signal_history['history_cover_signal'][-1] == 1:
        return_signal.append('cover')

    return return_signal


def signal_pair_trade(future_A, future_B, point_A, point_B, prices_A, price_B,
                      signal_history, ols_const, ols_coef, threshold):
    # initial output data setting
    signal = {'time': time.strftime("%Y-%m-%d %I:%M:%S", time.localtime()), 'future_A': future_A, 'future_B': future_B,
              'prices_A_short': prices_A, 'prices_B_long': price_B, 'spread': None, 'buy': 0, 'short': 0, 'sell': 0,
              'cover': 0}

    # renew output data
    now_spread = price_B * point_B - ols_coef * prices_A * point_A - ols_const
    signal['spread'] = round(now_spread)

    # load history spread data
    history_spread = signal_history['history_spread']

    # buy part
    if now_spread < -threshold:
        signal['buy'] = 1

    # short part
    if now_spread > threshold:
        signal['short'] = 1

    # sell part
    if (history_spread[-1] < 0) & (now_spread >= 0):
        signal['sell'] = 1

    # cover part
    if (history_spread[-1] > 0) & (now_spread <= 0):
        signal['cover'] = 1

    return signal


def signal_history_record(signal, signal_history):
    # 把訊號寫入歷史資料
    global count
    count += 1
    if (signal_history['future_A'] == signal['future_A']) & (signal_history['future_A'] == signal['future_A']):
        signal_history['history_spread'].append(signal['spread'])
        signal_history['history_spread'].pop(0)

        signal_history['history_buy_signal'].append(signal['buy'])
        signal_history['history_buy_signal'].pop(0)

        signal_history['history_short_signal'].append(signal['short'])
        signal_history['history_short_signal'].pop(0)

        signal_history['history_sell_signal'].append(signal['sell'])
        signal_history['history_sell_signal'].pop(0)

        signal_history['history_cover_signal'].append(signal['cover'])
        signal_history['history_cover_signal'].pop(0)
        write_data_by_json(signal=signal_history, filename=f'{signal_history_file_name}{date_today}')
        if count % 50 == 0:
            print(signal_history)
            count = 0
    else:
        # 防呆裝置，避免資料輸入錯誤
        print('Record error on signal history data!')

    return signal_history


def write_data_by_json(signal, filename, mode='a'):
    filename_latest = filename + "_latest.txt"
    # filename_latest = "signal_history_2023_04_25_latest.txt"
    filename = filename + ".txt"
    with open(filename, mode) as temp_txt_file:
        temp_txt_file.write(json.dumps(signal))
        temp_txt_file.write("\n")

    with open(filename_latest, 'w') as file:
        json.dump(signal, file)
