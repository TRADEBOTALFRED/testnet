import decimal
import time

from service import data_cache
from service.data_cache import get_timeframe_5min
from service.models import *
from .markets import binance_api

from datetime import datetime, timedelta
from django.utils import timezone
import random

MAX_DOWNLOADS_PER_TIME = 10
available_to_download_per_time = MAX_DOWNLOADS_PER_TIME


def get_start_timestamp(timestamp, timeframe):
    frame_sec = timeframe.seconds()
    return int(timestamp / frame_sec) * frame_sec - frame_sec


def cron_task():
    print('task')
    global available_to_download_per_time
    available_to_download_per_time = MAX_DOWNLOADS_PER_TIME
    timestamp = int(time.time())
    load_5m_for(timestamp, True)


def load_retro_task(request):
    # print('load retro task')
    # timestamp = int(time.time())
    # delta = request.GET.get('delta')
    # if delta is None or len(delta) == 0:
    #     delta = '24'
    # delta = int(delta)
    # d = timedelta(hours=delta).total_seconds()
    # for i in range(0, 400):
    #     timestamp -= d
    #     load_5m_for(timestamp, False)
    global available_to_download_per_time
    available_to_download_per_time = MAX_DOWNLOADS_PER_TIME*10
    m5 = get_timeframe_5min()
    #indexes = PairIndex.objects.filter(timeframe=m5).all()
    indexes = data_cache.get_pair_indexes(m5)
    data = PairData.objects.filter(pair_index__in=indexes).all()
    print('Total 5m: ', len(data))
    print('Total others: ', len(PairData.objects.exclude(pair_index__in=indexes).all()))
    ts = {}
    tss = []
    for d in data:
        ts[d.open_time.timestamp()] = 0
    for t in ts.keys():
        tss.append(t)
    tss.sort()
    for i in range(0, 10000):
        ind = random.randint(0, len(tss))
        t = tss[ind]
        print(t, ind)
        #if t < 1503079800.0:
        #    continue
        available_to_download_per_time = MAX_DOWNLOADS_PER_TIME * 10
        load_5m_for(t, True)
        # data_loader.aggregate_all(t)
        # time.sleep(5)


def load_5m_for(timestamp, aggregate):
    timeframe = get_timeframe_5min()
    start_ts = get_start_timestamp(timestamp, timeframe)

    download_all_pairs(start_ts, timeframe)
    if aggregate:
        aggregate_all(timestamp)


def download_all_pairs(start_ts, timeframe):
    for pair in data_cache.get_all_pairs():
        get_and_save_candle(pair, timeframe, start_ts)


def aggregate_all(timestamp):
    for timeframe in Timeframe.objects.all():
        if timeframe.pk != 1:
            aggregate_timeframe(timeframe, timestamp)


def aggregate_timeframe(timeframe, timestamp):
    # пришло ли время?
    start_ts = get_start_timestamp(timestamp, timeframe)
    end_ts = start_ts + timeframe.seconds()
    # print(timeframe, timestamp_to_datetime(start_ts), timestamp_to_datetime(end_ts))
    if timestamp < end_ts + 100:
        #print('not ready')
        return
    for pair in data_cache.get_all_pairs():
        if is_pair_data_exists(pair, timeframe, start_ts):
            #print('already exists')
            continue
        #print('aggregating..')
        try_aggregate_pair_data(timeframe, pair, start_ts, end_ts)


def is_pair_data_exists(pair, timeframe, timestamp):
    return data_cache.get_pair_data(pair, timeframe, timestamp) is not None




def get_and_save_candle(pair, timeframe, start_ts):
    res = data_cache.get_pair_data(pair, timeframe, start_ts)
    if res is not None:
        #print('found')
        return res
    else:
        print('create')
        #pair_index, created = PairIndex.objects.get_or_create(pair=pair, timeframe=timeframe)
        pair_index = data_cache.get_pair_index(pair, timeframe)
        #print("?", pair_index, created)
        candle = get_candle(pair, timeframe, start_ts, pair_index)
        print('candle=', candle)
        if candle is None:
            return None
        pair_data = PairData.create_from(candle)
        pair_data.save()
        return pair_data


def get_candle(pair, timeframe, start_ts, pair_index):
    market_name = pair.market.name

    if market_name == 'Binance':
        return binance_api.get_candle(pair, timeframe, start_ts, pair_index)


def aggregate_candle(parts, pair_index):
    res = PairData()
    res.pair_index = pair_index
    res.open_time = parts[0].open_time
    res.open_price = parts[0].open_price
    res.high_price = parts[0].high_price
    res.low_price = parts[0].low_price
    res.close_price = parts[-1].close_price
    res.volume = 0
    res.close_time = parts[-1].close_time

    for part in parts:
        res.high_price = res.high_price.max(part.high_price)
        res.low_price = res.low_price.min(part.low_price)
        res.volume += part.volume
    return res


def try_aggregate_pair_data(timeframe, pair, start_ts, end_ts):
    # if timeframe.pk > 5:
    #     return
    part_frame = get_timeframe_5min()
    #    print(timeframe, '->', part_frame)

    subpairs = []
    for ts in range(start_ts, end_ts, part_frame.seconds()):
        part_pair = data_cache.get_pair_data(pair, part_frame, ts)
        if part_pair is None:
            global available_to_download_per_time
            if available_to_download_per_time > 0:
                available_to_download_per_time -= 1
                print('download more', ts)
                part_pair = get_and_save_candle(pair, part_frame, ts)
        if part_pair is None:
            return
        subpairs.append(part_pair)
    #pair_index = PairIndex.objects.get(pair=pair, timeframe=timeframe)
    pair_index = data_cache.get_pair_index(pair, timeframe)
    candle = aggregate_candle(subpairs, pair_index)
    print('=>', candle)
    candle.save()
    aggregate_all(candle.open_time.timestamp())
