from django.conf.urls import url, include
from scale.views import *

urlpatterns=[
    url(r'/(?P<device_id>\w+)', create_ticket),
    url(r'^lots/(?P<ticket_id>[0-9a-f-]+)', get_lots),
    url(r'^crops/(?P<ticket>[0-9a-f-]+)', get_crops)
]