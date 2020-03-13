# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


"""
Model class for the costumer data.
"""
class Costumer(models.Model):

    name = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    age  = models.IntegerField(
        blank=False, null=False,
        validators=[
            MaxValueValidator(150),
            MinValueValidator(1)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=False, null=True)

    def __str__(self):
        return self.name