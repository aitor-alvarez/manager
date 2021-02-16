# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

category_choices=(
('T', 'Trap'),
('V','Vehicle'),
('N','Non Registered (Tractor, Farm Uses)'),
)


class Item(models.Model):
    category = models.CharField(choices=category_choices, max_length=1, verbose_name='Category', blank=False, null=True)
    type = models.CharField(max_length=200, verbose_name='Group')
    code = models.CharField(max_length=200, verbose_name='ID', blank=True, null=True)
    description = models.CharField(max_length=200, verbose_name='Description', blank=False, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    license = models.CharField(max_length=200, blank=True, null=True)
    plate = models.CharField(max_length=200, blank=True, null=True)
    make = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    vin_serial = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=200, blank=True, null=True)
    insurance_expires = models.DateField( blank=True, null=True)
    insurance = models.CharField(max_length=200, blank=True, null=True)
    safety_expires= models.DateField( blank=True, null=True)
    registration_expires= models.DateField( blank=True, null=True)
    registration_amount = models.FloatField( blank=True, null=True)
    tire_front = models.CharField(max_length=200, blank=True, null=True)
    tire_back = models.CharField(max_length=200, blank=True, null=True)
    tare = models.CharField(max_length=200, blank=True, null=True)
    next_check_in_days = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, blank=True)

    def get_absolute_url(self):
        return "/items/view/%i/" % self.id

    def check_status(self):
        limit = self.created + datetime.timedelta(days=int(self.next_check_in_days))
        if datetime.datetime.now() >= limit:
            return True
        else:
            return False

    def __unicode__(self):
        return str(self.type)


class Service(models.Model):
    vehicle = models.ForeignKey(Item)
    service_date = models.DateField(blank=False)
    service_type = models.CharField(max_length=200, blank=False, null=True)
    mileage = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-service_date']

    def __unicode__(self):
        return str(self.vehicle.type)+' '+str(self.service_date)
