# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url, include
from .views import index

urlpatterns = [
    # ЗАЙТИ ПОД ПОЛЬЗОВАТЕЛЕМ - будет редиректиться сюда! name - обязателен!
    url(r'', index, name='index'),
]
