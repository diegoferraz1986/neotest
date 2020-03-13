# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import render


class IndexView(View):
    """
    View class for the main page of the application.
    """
    TEMPLATE = 'costumer/index.html'

    def get(self, request):

        """ GET request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :rtype: django.http.response.HttpResponse
        """
        return render(request, self.TEMPLATE, {})
