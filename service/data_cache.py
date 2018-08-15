from django.utils import timezone
from django.core.cache import cache
from datetime import datetime, timedelta
from django.utils import timezone


from service.models import Timeframe, Pair, PairIndex, PairData


def timestamp_to_datetime(ts):
    dt = datetime.fromtimestamp(int(ts))
    return timezone.make_aware(dt, timezone.utc)


def get_timeframe_5min():
    m5 = cache.get('timeframe_5min')
    if m5 is None:
        m5 = Timeframe.objects.get(pk=1)
        cache.set('timeframe_5min', m5)
    return m5


def get_all_pairs():
    pairs = cache.get('pairs_all')
    if pairs is None:
        pairs = Pair.objects.all()
        cache.set('pairs_all', pairs)
    return pairs


def get_pair_index(pair, timeframe):
    key = 'pair_index_' + str(pair.pk) + '_' + str(timeframe.pk)
    pair_index = cache.get(key)
    if pair_index is None:
        pair_index, created = PairIndex.objects.get_or_create(pair=pair, timeframe=timeframe)
        cache.set(key, pair_index)

    return pair_index


def get_pair_indexes(timeframe):
    key = 'all_pair_indexes_' + str(timeframe.pk)
    indexes = cache.get(key)
    if indexes is None:
        indexes = PairIndex.objects.filter(timeframe=timeframe).all()
        cache.set(key, indexes)

    return indexes


def get_pair_data(pair, timeframe, timestamp):
    pair_index = get_pair_index(pair, timeframe)
    key = 'pair_data_' + str(pair_index.pk) + '_' + str(timestamp)
    data = cache.get(key)
    if data is None:
        data = load_pair_data(pair_index, timestamp)
        cache.set(key, data)

    return data


def load_pair_data(pair_index, timestamp):
    # pair_index, created = PairIndex.objects.get_or_create(pair=pair, timeframe=timeframe)
    # pair_index = get_pair_index(pair, timeframe)
    try:
        # TODO временный костыль, таких ошибок возникать не должно
        if len(PairData.objects.filter(pair_index=pair_index, open_time=timestamp_to_datetime(timestamp)).all()) > 1:
            first = True
            for p in PairData.objects.filter(pair_index=pair_index, open_time=timestamp_to_datetime(timestamp)).all():
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:::", p)
                if first:
                    first = False
                else:
                    p.delete()
        return PairData.objects.get(pair_index=pair_index, open_time=timestamp_to_datetime(timestamp))
    except PairData.DoesNotExist:
        return None
