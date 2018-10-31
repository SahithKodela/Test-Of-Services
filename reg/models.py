# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from sqlserver_ado.models import RawStoredProcedureManager

class Register(models.Model):
    user = models.CharField(max_length=20)
    address = models.CharField(max_length=120)
    dob = models.CharField(max_length=10)
    objects = RawStoredProcedureManager()

# Create your models here.
