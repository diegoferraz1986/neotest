# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from costumer.views.views import IndexView
from costumer.views.api import ApiCostumerListView, ApiCostumerDetailView

app_name = 'costumer'

urlpatterns = [
    # Main page
    url(r'^$', IndexView.as_view(), name='index'),
    # Apis
    url(r'^api/v1/costumer/$', ApiCostumerListView.as_view(), name='api_v1_costumer'),
    url(r'^api/v1/costumer/(?P<pk>[0-9]+)/$', ApiCostumerDetailView.as_view(), name='api_v1_costumer_detail'),
]