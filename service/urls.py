from django.urls import path
from django.http import JsonResponse

from . import views

urlpatterns = [
    path('cron/', views.tasks, name='tasks'),
    path('retro/', views.retro_tasks, name='retro_tasks'),
    path('candles/', views.candles_list, name='list')
]


