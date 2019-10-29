from fastapi import FastAPI
from enum import Enum
from starlette.responses import PlainTextResponse
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

app = FastAPI()

@app.get("/feed/{candle}/{start_time}/{end_time}", response_class=PlainTextResponse)
def read_item(candle: Candle = 'M5', start_time: int = 1572258336, end_time: int = 1572344736, q: str = 'Volatility 75 Index'):
    feed = get_feed(q, start_date=start_time, end_date=end_time, candle_type=candle)
    return feed
