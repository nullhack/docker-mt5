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

dict_ticks = {
    'ALL':MT5_COPY_TICKS_ALL,
    'INFO':MT5_COPY_TICKS_INFO,
    'TRADE':MT5_COPY_TICKS_TRADE
}

def get_ohlc(symbol, start_dtm=None, end_dtm=None, candle_type='H1'):
    if not end_dtm: end_dtm = pandas.to_datetime('now')
    if not start_dtm: start_dtm = pandas.to_datetime(end_dtm) - pandas.to_timedelta('1 day')

    try:
        start_dtm = pandas.to_datetime(start_dtm, unit='s')
    except:
        start_dtm = pandas.to_datetime(start_dtm)

    try:
        end_dtm = pandas.to_datetime(end_dtm, unit='s')
    except:
        end_dtm = pandas.to_datetime(end_dtm)

    try:
        '''Fetch data from MT5 and put on a dataframe'''
        rate = MT5CopyRatesRange(symbol, dict_timeframe[candle_type], start_dtm, end_dtm)
        feed = pandas.DataFrame(list(rate), columns=['time','open','high','low','close','tick_volume','spread','real_volume'])
        feed['symbol'] = symbol
        feed_output = io.StringIO()
        feed.to_csv(feed_output, index=False)
        return feed_output.getvalue()
    except Exception as err:
        print('>>> ERROR:', err, symbol)

    return pandas.DataFrame([], columns=['time','open','high','low','close','tick_volume','spread','real_volume'])


def get_tick(symbol, start_dtm=None, end_dtm=None, tick_type='ALL'):
    if not end_dtm: end_dtm = pandas.to_datetime('now')
    if not start_dtm: start_dtm = pandas.to_datetime(end_dtm) - pandas.to_timedelta('1 minute')

    try:
        start_dtm = pandas.to_datetime(start_dtm, unit='s')
    except:
        start_dtm = pandas.to_datetime(start_dtm)

    try:
        end_dtm = pandas.to_datetime(end_dtm, unit='s')
    except:
        end_dtm = pandas.to_datetime(end_dtm)

    try:
        '''Fetch data from MT5 and put on a dataframe'''
        rate = MT5CopyTicksRange(symbol, start_dtm, end_dtm, dict_ticks[tick_type])
        feed = pandas.DataFrame(list(rate), columns=['time','bid','ask','last','volume','flags'])
        feed['symbol'] = symbol
        feed_output = io.StringIO()
        feed.to_csv(feed_output, index=False)
        return feed_output.getvalue()
    except Exception as err:
        print('>>> ERROR:', err, symbol)

    return pandas.DataFrame([], columns=['time','bid','ask','last','volume','flags'])

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'symbol',
        help="symbol string as defined on mt5 terminal, default='Volatility 75 Index'", default='Volatility 75 Index'
    )
    parser.add_argument(
        '-s',
        '--start_dtm',
        action='store',
        dest='start_dtm',
        help="start dtm (either unix epoch or string), default='5 mintues ago'",
        default=pandas.to_datetime('now') - pandas.to_timedelta('5 minutes')
    )
    parser.add_argument(
        '-e',
        '--end_dtm',
        action='store',
        dest='end_dtm',
        help="end dtm (either unix epoch or string), default='now'",
        default=pandas.to_datetime('now')
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-c',
        '--candle_type',
        action='store',
        dest='candle_type',
        choices=list(dict_timeframe.keys()),
        help="timeframe for candles, choose from the list of options available",
    )
    group.add_argument(
        '-t',
        '--tick_type',
        action='store',
        dest='tick_type',
        choices=list(dict_ticks.keys()),
        help="ticks that will be copied",
    )
    args = parser.parse_args()

    if args.candle_type: print(get_feed(args.symbol, args.start_dtm, args.end_dtm, args.candle_type))
    elif args.tick_type: print(get_tick(args.symbol, args.start_dtm, args.end_dtm, args.tick_type))
