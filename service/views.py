from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from logging import getLogger
from . import data_loader


logger = getLogger(__name__)


@csrf_exempt
def tasks(request):
    data_loader.cron_task()
    return JsonResponse({}, status=302)
    #return _post_tasks(request)
    # if request.method == 'POST':
    #     return _post_tasks(request)
    # else:
    #     return JsonResponse({}, status=405)


