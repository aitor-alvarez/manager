from django.conf.urls import url, include
from planner.views import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [

url(r'^plans', login_required(PlanView.as_view()), name='plans'),
url(r'^plan/(?P<plan_id>\d+)/parts/$', get_planparts, name='planparts'),
url(r'^plan/(?P<plan_id>\d+)/edit/$', get_planparts, name='planparts'),
url(r'^new/plan/', login_required(CreatePlanView.as_view()), name='createplanview'),
url(r'^delete/plan/(?P<part_id>\d+)/$', delete_plan_in_part, name='delete_parts'),
url(r'^calendar', login_required(index), name='index'),
url(r'^all_events/', login_required(all_events), name='all_events'),
url(r'^update_parts/', update_part, name='update_part' ),

]
