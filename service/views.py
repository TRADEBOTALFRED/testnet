from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from . import data_loader
from .models import PairData, PairIndex, Pair, Timeframe

logger = getLogger(__name__)


@csrf_exempt
def tasks(request):
    data_loader.cron_task()
    return JsonResponse({}, status=302)
    # return _post_tasks(request)
    # if request.method == 'POST':
    #     return _post_tasks(request)
    # else:
    #     return JsonResponse({}, status=405)


def retro_tasks(request):
    data_loader.load_retro_task(request)
    return JsonResponse({}, status=302)


def candles_list(request):
    pair_name = request.GET.get('pair')
    if pair_name is not None and len(pair_name) == 0:
        pair_name = None
    timeframe_min = request.GET.get('timeframe')
    if timeframe_min is not None and len(timeframe_min) == 0:
        timeframe_min = None
    from_date = request.GET.get('from_date')
    if from_date is not None and len(from_date) == 0:
        from_date = None

    res = PairData.objects
    if from_date is not None:
        res = res.filter(open_time__gte=from_date)
    if pair_name is not None:
        pair = Pair.objects.get(name=pair_name)
        if timeframe_min is None:
            pair_indexes = PairIndex.objects.filter(pair=pair).all()
            res = res.filter(pair_index__in=pair_indexes)
        else:
            timeframe = Timeframe.objects.get(minutes=timeframe_min)
            print('tf=', timeframe)
            pair_indexes = PairIndex.objects.get(pair=pair, timeframe=timeframe)
            res = res.filter(pair_index=pair_indexes)

    res = res.order_by('open_time')

    limit = request.GET.get('limit')
    if limit is not None and len(limit) > 0:
        res = res[:int(limit)]

    return render(request, 'data/list.html', {'candles': res})


