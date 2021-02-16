from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^create$', CreateItem.as_view(), name='create_item'),

    url(r'^$', show_items, name='view_items'),
    url(r'^edit/(?P<item_id>\d+)/$', update_item, name='create_view'),
    url(r'^view/(?P<item_id>\d+)/$', show_item, name='view_item'),
    url(r'^new_service/(?P<item_id>\d+)/$', CreateService.as_view(), name='new_service'),
    url(r'edit_service/(?P<service_id>\d+)/$', update_service, name='update_service'),
		url(r'search/$', SearchView.as_view(), name='search_item')

]