from fastapi import FastAPI
from enum import Enum
from starlette.responses import PlainTextResponse
from datetime import datetime
from pymt5 import *

class Candle(str, Enum):
    M1='M1'
    M2='M2'
    M3='M3'
    M4='M4'
    M5='M5'
    M6='M6'
    M10='M10'
    M12='M12'
    M15='M15'
    M20='M20'
    M30='M30'
    H1='H1'
    H2='H2'
    H3='H3'
    H4='H4'
    H6='H6'
    H8='H8'
    H12='H12'
    D1='D1'
    W1='W1'
    MON1='MON1'

app = FastAPI(
    title="MT5 feed API",
    description="This API provides REST API for MetaTrader5 API (Python based API to retrieve feed data from MT5 client platform)",
    version="1.0.0",
    )

@app.get("/health")
def health():
    feed = get_ohlc('EURUSD', candle_type='D1')
    return {'healthy': True if len(feed) else False}

@app.get("/tick", response_class=PlainTextResponse)
def api_get_tick(start_dtm: str = str(datetime.now()-pandas.to_timedelta('5 minutes')), end_dtm: str = str(datetime.now()), symbol: str = 'EURUSD'):
    feed = get_tick(symbol, start_dtm=start_dtm, end_dtm=end_dtm)
    return feed

@app.get("/tick/{start_dtm}/{end_dtm}", response_class=PlainTextResponse)
def api_get_tick_epoch(start_dtm: int = 1572344136, end_dtm: int = 1572344736, symbol: str = 'EURUSD'):
    feed = get_tick(symbol, start_dtm=start_dtm, end_dtm=end_dtm)
    return feed

@app.get("/ohlc/{candle}", response_class=PlainTextResponse)
def api_get_ohlc(candle: Candle = 'M5', start_dtm: str = str(datetime.now().date()), end_dtm: str = str(datetime.now()), symbol: str = 'EURUSD'):
    feed = get_ohlc(symbol, start_dtm=start_dtm, end_dtm=end_dtm, candle_type=candle)
    return feed

@app.get("/ohlc/{candle}/{start_dtm}/{end_dtm}", response_class=PlainTextResponse)
def api_get_ohlc_epoch(candle: Candle = 'M5', start_dtm: int = 1572258336, end_dtm: int = 1572344736, symbol: str = 'EURUSD'):
    feed = get_ohlc(symbol, start_dtm=start_dtm, end_dtm=end_dtm, candle_type=candle)
    return feed
