# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from django.shortcuts import render

from rest_framework import status
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.paginator import Paginator

from costumer.models import Costumer
from costumer.serializers import CostumerSerializer

from django.db.models import Q

class ApiCostumerListView(APIView):

    """ View class for the api/v1/costumer/ route """

    def get_queryset(self, request):

        """ Build the query for the costumer list.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :rtype: rest_framework.serializers.ListSerializer, int
        """

        order_by = self.request.query_params.get('order_by', 'name')
        order = self.request.query_params.get('order', 'asc')
        if order == 'desc':
            order_by = '-' + order_by
        query = Costumer.objects.order_by(order_by)
        search = self.request.query_params.get('search')
        if (search):
            query = query.filter(
                Q(name__contains=search) |
                Q(city__contains=search) |
                Q(age__contains=search) |
                Q(id__contains=search)
            )
        total_records = query.count()
        page = self.request.query_params.get('page', 1)
        size = self.request.query_params.get('size', 10)
        paginator = Paginator(query, size)
        serializer = CostumerSerializer(paginator.page(page), many=True, context={'request':request})

        return serializer, total_records


    def get(self, request):

        """ GET request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :rtype: rest_framework.response.Response
        """
        costumers, total_records = self.get_queryset(request)
        total_pages = math.ceil(total_records / 10)

        return Response({'data': costumers.data, 'total_records': total_records, 'total_pages':  total_pages})

    def post(self, request):

        """ POST request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :rtype: rest_framework.response.Response
        """
        serializer = CostumerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiCostumerDetailView(APIView):

    """ Api view class for the api/v1/costumer/(?P<pk>[0-9]+)/ route. """

    def get_object(self, pk):
        """ Try to get the costumer by his primary key.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type pk: int
        :param pk: Primary key for the query

        :raises: Http404

        :rtype: costumer.models.Costumer
        """

        try:
            print(type(Costumer.objects.get(id=pk)))
            return Costumer.objects.get(id=pk)
        except Costumer.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        """ GET request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :type pk: int
        :param pk: Primary key for the query

        :rtype: rest_framework.response.Response
        """

        costumer = self.get_object(pk=pk)
        serializer = CostumerSerializer(costumer)
        return Response(serializer.data)

    def put(self, request, pk):

        """ PUT request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :type pk: int
        :param pk: Primary key for the query

        :rtype: rest_framework.response.Response
        """

        costumer = self.get_object(pk=pk)
        serializer = CostumerSerializer(costumer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        """ DELETE request for the route.

        :type self: costumer.views.api.ApiCostumerListView
        :param self:

        :type request: rest_framework.request.Request
        :param request:

        :type pk: int
        :param pk: Primary key for the query

        :rtype: rest_framework.response.Response
        """

        costumer = self.get_object(pk=pk)

        if costumer.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
