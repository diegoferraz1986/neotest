# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Implements REST serializers for models
"""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from costumer.models import Costumer


class CostumerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Costumer model
    """

    class Meta:
        model = Costumer
        fields = ('id', 'name', 'city', 'age', )
