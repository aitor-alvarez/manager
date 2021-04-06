# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import datetime


class RemoteUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	remote_user_code = models.CharField(max_length=155)

	def __str__(self):
		return str(self.remote_user_code)

class ScaleRecords(models.Model):
	sheet_id = models.CharField(max_length=155, null=False, blank=False, unique=False)
	displayed_weight = models.DecimalField(max_digits=4, decimal_places=3, null=False, blank=False)
	unit = models.CharField(default='lb', max_length=25, null=False, blank=False)
	time_stamp = models.CharField(max_length=155, null=False, blank=False)
	user = models.CharField(default=None, max_length=155, null=True, blank=False)
	lot = models.CharField(default=None, max_length=155, null=True, blank=False)
	crop = models.CharField(default=None, max_length=155, null=True, blank=False)
	created = models.DateField(default=datetime.datetime.now())
	error_log = models.TextField()

	def __str__(self):
		return str(self.sheet_id)+' '+str(self.created)

