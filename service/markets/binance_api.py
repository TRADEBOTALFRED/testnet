import decimal
from datetime import datetime

from binance import client
from binance.client import Client
import binance.helpers
from service.models import PairIndex, PairData
from django.utils import timezone

binance_api_client = Client("", "")

binance_candles_cache = {}


def timestamp_to_datetime(ts):
    dt = datetime.fromtimestamp(int(ts))
    return timezone.make_aware(dt, timezone.utc)


def interval_from_timeframe(timeframe):
    # TODO check interval
    m = timeframe.minutes
    if m < 60:
        return "%dm" % m
    elif m < 24 * 60:
        return "%dh" % (m / 60)
    elif m < 7 * 24 * 60:
        return "%dd" % (m / 60 / 24)


def get_candle(pair, timeframe, start_ts, pair_index):
    # api = Client("", "")
    assert timeframe.minutes == 5
    from_cache = _find_in_cache(pair, start_ts)
    if from_cache is None:
        data = binance_api_client.get_klines(
            symbol=pair.name,
            interval=interval_from_timeframe(timeframe),
            limit=500,
            startTime=start_ts * 1000,
            endTime=None
        )
        if len(data) < 1:
            return None
        binance_candles_cache[pair.name] = data
        rec = data[0]
        binance_candles_cache[pair.name].pop()
    else:
        # print('binance-hit!')
        # data = binance_api_client.get_klines(
        #     symbol=pair.name,
        #     interval=interval_from_timeframe(timeframe),
        #     limit=1,
        #     startTime=start_ts * 1000,
        #     endTime=None
        # )
        # r0 = data[0]
        # assert r0[0] == from_cache[0]
        # assert r0[1] == from_cache[1]
        # assert r0[2] == from_cache[2]
        # assert r0[3] == from_cache[3]
        # assert r0[4] == from_cache[4]
        # assert r0[5] == from_cache[5]
        # assert r0[6] == from_cache[6]
        rec = from_cache
    # print(data)
    # assert 1 <= len(data) <= 2
    res = PairData()
    res.pair_index = pair_index
    open_time = round(rec[0] / 1000)
    if open_time != start_ts:
        print('Wrong binance result!  (length =', len(data), ')')
        print('open_time (from response):', open_time, timestamp_to_datetime(open_time))
        print('start_ts (requested):', start_ts, timestamp_to_datetime(start_ts))
        print('\n')
        return None
    assert open_time == start_ts
    res.open_time = timestamp_to_datetime(open_time)
    res.open_price = decimal.Decimal(rec[1])
    res.high_price = decimal.Decimal(rec[2])
    res.low_price = decimal.Decimal(rec[3])
    res.close_price = decimal.Decimal(rec[4])
    res.volume = decimal.Decimal(rec[5])
    res.close_time = timestamp_to_datetime(round(rec[6] / 1000))

    return res


def _find_in_cache(pair, start_ts):
    global binance_candles_cache
    if pair.name not in binance_candles_cache:
        binance_candles_cache[pair.name] = []
        return None
    cache = binance_candles_cache[pair.name]
    for rec in cache:
        open_time = round(rec[0] / 1000)
        if open_time == start_ts:
            return rec
