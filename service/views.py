from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from . import data_loader
from .models import PairData

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
    #candles = PairData.objects.filter(open_time=timezone.now()).order_by('open_time')
    candles = PairData.objects.order_by('open_time')
    print(len(candles))
    return render(request, 'data/list.html', {'candles': candles})
