from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from . import data_loader
from .models import PairData, PairIndex, Pair

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


def candles_list(request):
    pair_name = request.GET.get('pair')
    print(pair_name)
    if pair_name is None or len(pair_name.strip()) == 0:
        #candles = PairData.objects.filter(open_time=timezone.now()).order_by('open_time')
        candles = PairData.objects.order_by('open_time')
    else:
        pair = Pair.objects.get(name=pair_name)
        pair_indexes = PairIndex.objects.filter(pair=pair).all()
        candles = PairData.objects.filter(pair_index__in=pair_indexes).order_by('open_time')
    print(len(candles))
    return render(request, 'data/list.html', {'candles': candles})
