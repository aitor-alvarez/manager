from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.views.generic.edit import UpdateView, CreateView
from .models import *
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from .utils import plans_to_json
from manager.models import Lot, Crop
import datetime
import json

class PlanView(ListView):
	template_name = 'planner/plans.html'
	context_object_name = 'plans'
	queryset = Plan.objects.all()

@login_required
def get_planparts(request, plan_id):
	parts = PlanPart.objects.filter(plan= plan_id)
	return render(request, 'planner/plan_parts.html', {'parts': parts})

class CreatePlanView(CreateView):
	form_class = PlanForm
	template_name = 'planner/create_plan_form.html'
	success_url = '/pests'

	def form_valid(self, form):
		plan_types = ['P','PL','V','H', 'C']
		plan = form.save(commit=False)
		date = form.cleaned_data['start_date']
		crop = form.cleaned_data['crop']
		part_date = PlanTemplate.objects.get(crop=crop)
		plan.save()
		for p in plan_types:
			if p =='P':
				prop_end_date = date + datetime.timedelta(days=part_date.days_propagation)
				plan_part = PlanPart(plan= plan, plan_type = p, begin=date, end = prop_end_date)
				plan_part.save()
			elif p=='PL':
				plant_start_date = prop_end_date + datetime.timedelta(days=1)
				plant_end_date = plant_start_date + datetime.timedelta(days=part_date.days_planting)
				plan_part = PlanPart(plan= plan, plan_type = p, begin= plant_start_date, end= plant_end_date)
				plan_part.save()
			elif p=='V':
				veg_start_date = plant_end_date + datetime.timedelta(days=1)
				veg_end_date = veg_start_date + datetime.timedelta(days=part_date.days_vegetative)
				plan_part = PlanPart(plan= plan, plan_type = p, begin= veg_start_date, end = veg_end_date)
				plan_part.save()
			elif p=='H':
				harv_start_date = veg_end_date + datetime.timedelta(days=1)
				harv_end_date = harv_start_date + datetime.timedelta(days=part_date.days_harvest)
				plan_part = PlanPart(plan= plan, plan_type = p, begin= harv_start_date, end= harv_end_date)
				plan_part.save()
			elif p=='C':
				clean_start_date = harv_end_date + datetime.timedelta(days=1)
				clean_end_date = clean_start_date + datetime.timedelta(days=part_date.days_cleaning)
				plan_part = PlanPart(plan= plan, plan_type = p, begin= clean_start_date, end= clean_end_date)
				plan_part.save()

		return HttpResponseRedirect('/planner/calendar')

@login_required
def index(request):
	if request.method == "POST" :
		if 'field' in request.POST:
			fields = Lot.objects.order_by('lot_name')
			crops = Crop.objects.order_by('name')
			field_id = request.POST['field']
			event_url = 'events_field/'+str(field_id)+'/'
			plans = event_in_field(request, field_id=field_id)
			return render(request, 'planner/chart.html', {'fields':fields, 'crops':crops, 'plans': plans })
		if 'crop' in request.POST:
			fields = Lot.objects.order_by('lot_name')
			crops = Crop.objects.order_by('name')
			crop_id = request.POST['crop']
			plans = event_in_field(request, crop_id=crop_id)
			return render(request, 'planner/chart.html', {'fields':fields, 'crops':crops, 'plans': plans })
		else:
			fields = Lot.objects.order_by('lot_name')
			crops = Crop.objects.order_by('name')
			field_id = request.POST['field']
			crop_id = request.POST['crop']
			plans = event_in_field(request, field_id, crop_id)
			return render(request, 'planner/chart.html', {'fields':fields, 'crops':crops, 'plans': plans })
	else:
		fields = Lot.objects.order_by('lot_name')
		crops = Crop.objects.order_by('name')
		return render(request, 'planner/chart.html', {'fields':fields, 'crops':crops })

@login_required
def all_events(request):
	plans = PlanPart.objects.all()
	return plans_to_json(plans)

@login_required
def event_in_field(request, field_id=None, crop_id=None):
	today = datetime.date.today()-datetime.timedelta(days=60)
	if field_id is not None:
		get_plan_field= Plan.objects.filter(field=field_id, start_date__gte=today)
		parts = PlanPart.objects.filter(plan__in=get_plan_field)
		return plans_to_json(parts)
	if crop_id is not None:
		get_crop_field= Plan.objects.filter(crop=crop_id, start_date__gte=today)
		parts = PlanPart.objects.filter(plan__in=get_crop_field)
		return plans_to_json(parts)
	elif field_id is not None and crop_id is not None:
		get_field= Plan.objects.filter(crop=crop_id, field=field_id, start_date__gte=today)
		parts = PlanPart.objects.filter(plan__in=get_field)
		return plans_to_json(parts)

@login_required
def update_part(request):
	if request.is_ajax():
		parts = json.loads(request.POST.get('tasks', []))
		for p in parts:
			part_id = PlanPart.objects.get(pk=p['id'])
			if 'Propagation' in p['name']:
				plan = Plan.objects.get(pk=part_id.plan.id)
				plan.start_date = p['start']
				plan.save()
			part_id.begin = p['start']
			part_id.end = p['end']
			part_id.save()
        return HttpResponse("OK")

@login_required
def delete_plan_in_part(request, part_id):
	part = PlanPart.objects.get(pk=part_id)
	if request.method =='POST':
		parts = PlanPart.objects.filter(plan=part.plan)
		parts.delete()
		part.plan.delete()
		return HttpResponseRedirect('/planner/calendar')
	return render(request, 'planner/delete_plan.html', {'part':part})

