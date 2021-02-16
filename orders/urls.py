from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<day>\d\d)$', views.main, name='main'),
    url(r'^change_order$',views.change_order, name='change_order'),
    url(r'^change_pallette$',views.change_pallette, name='change_pallette'),
    url(r'^change_po$',views.change_po, name='change_po'),
    url(r'^change_note$',views.change_note, name='change_note'),
    url(r'^add_order$',views.add_order, name='add_order'),
    url(r'^history',views.history, name='get_history'),
    url(r'^recurring$',views.get_recurring_orders, name='get_recurring_orders'),
    url(r'^delete_order$',views.delete_order, name='delete_order'),
    url(r'^delete_recurring_order$',views.delete_recurring_order, name='delete_order'),
    url(r'^trace_orders/(?P<date>\d{4}-\d{2}-\d{2})/$',views.trace_orders, name='trace_orders'),
    url(r'^get_orders/$',views.get_labels_orders, name='get_order'),
    url(r'^get_labels/$', views.get_labels, name='create_label'),
]
