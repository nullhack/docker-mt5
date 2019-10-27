from datetime import datetime
from MetaTrader5 import *
import pandas
import time
import io

MT5Initialize("C:\\Program Files\\MetaTrader 5\\terminal64.exe")
MT5WaitForTerminal()

dict_timeframe = {
    'M1':MT5_TIMEFRAME_M1,
    'M2':MT5_TIMEFRAME_M2,
    'M3':MT5_TIMEFRAME_M3,
    'M4':MT5_TIMEFRAME_M4,
    'M5':MT5_TIMEFRAME_M5,
    'M6':MT5_TIMEFRAME_M6,
    'M10':MT5_TIMEFRAME_M10,
    'M12':MT5_TIMEFRAME_M12,
    'M15':MT5_TIMEFRAME_M15,
    'M20':MT5_TIMEFRAME_M20,
    'M30':MT5_TIMEFRAME_M30,
    'H1':MT5_TIMEFRAME_H1,
    'H2':MT5_TIMEFRAME_H2,
    'H3':MT5_TIMEFRAME_H3,
    'H4':MT5_TIMEFRAME_H4,
    'H6':MT5_TIMEFRAME_H6,
    'H8':MT5_TIMEFRAME_H8,
    'H12':MT5_TIMEFRAME_H12,
    'D1':MT5_TIMEFRAME_D1,
    'W1':MT5_TIMEFRAME_W1,
    'MON1':MT5_TIMEFRAME_MON1,
}

def get_feed(symbol, start_date=pandas.to_datetime('now').date(), end_date=pandas.to_datetime('now'), candle_type='M1'):
    try:
        start_date = pandas.to_datetime(start_date, unit='s')
    except:
        start_date = pandas.to_datetime(start_date)

    try:
        end_date = pandas.to_datetime(end_date, unit='s')
    except:
        end_date = pandas.to_datetime(end_date)

    try:
        '''Fetch data from MT5 and put on a dataframe'''
        rate = MT5CopyRatesRange(symbol, dict_timeframe[candle_type], start_date, end_date)
        feed = pandas.DataFrame(list(rate), columns=['time','open','low','high','close','tick_volume','spread','real_volume'])
        feed['symbols'] = symbol
        feed_output = io.StringIO()
        feed.to_csv(feed_output, index=False)
        return feed_output.getvalue()
    except Exception as err:
        print('>>> ERROR:', err, symbol)

    return None

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'symbol',
        help="symbol string as defined on mt5 terminal, default='Volatility 75 Index'", default='Volatility 75 Index'
    )
    parser.add_argument(
        '-s',
        '--start_date',
        action='store',
        dest='start_date',
        help="start date (either unix epoch or string), default='now' (date part)",
        default=pandas.to_datetime('now').date()
    )
    parser.add_argument(
        '-e',
        '--end_date',
        action='store',
        dest='end_date',
        help="end date (either unix epoch or string), default='now'",
        default=pandas.to_datetime('now')
    )
    parser.add_argument(
        '-c',
        '--candle_type',
        action='store',
        dest='candle_type',
        choices=list(dict_timeframe.keys()),
        help="timeframe for candles, choose from the list of options available, default='D1'",
        default='D1'
    )
    args = parser.parse_args()

    print(get_feed(args.symbol, args.start_date, args.end_date, args.candle_type))
