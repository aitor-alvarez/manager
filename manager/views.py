from django.views.generic.base import TemplateView
from django.views.generic import ListView, FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .forms import *
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
import settings
import os, json
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

class HomeView(TemplateView):
	template_name = 'manager/home.html'


@permission_required('auth.add_user')
def signup_view(request):
		if request.method == 'POST':
				form = SignUpForm(request.POST)
				if form.is_valid():
						data = form.save(commit=False)
						data.email = form.cleaned_data['username']
						data.save()
						return redirect('/orders')
		else:
				form = SignUpForm()
		return render(request, 'registration/signup.html', {'form': form})



class LotView(ListView):
	template_name = 'manager/adminlot.html'
	context_object_name = 'adminlots'
	queryset = Lot.objects.all().extra(select={'case_insensitive_lot': 'lower(lot_name)'}).order_by(
		'case_insensitive_lot')


class CreateLot(CreateView):
	model = Lot
	fields = ['lot_name', 'rotation', 'crop', 'tax_code', 'county','acres']
	template_name = 'manager/create_lot_form.html'
	success_url = '/lots'

	def form_valid(self, form):
		lot = form.cleaned_data['lot_name']
		lot_exists = Lot.objects.filter(lot_name__iexact=lot)
		if lot_exists.count() > 0:
			return HttpResponseRedirect('/lot_exists')
		else:
			data = form.save(commit=False)
			data.lot_name = lot.upper()
			data.save()
			return super(CreateLot, self).form_valid(form)


class UpdateLot(UpdateView):
	model = Lot
	fields = ['lot_name', 'rotation', 'crop', 'acres', 'tax_code', 'county']
	template_name_suffix = '_update_form'
	success_url = '/lots'


class CropView(ListView):
	template_name = 'manager/admincrop.html'
	context_object_name = 'admincrops'
	queryset = Crop.objects.all()


class CreateCrop(CreateView):
	model = Crop
	fields = ['name']
	template_name = 'manager/create_crop_form.html'
	success_url = '/crops'


@login_required
def update_crop(request, crop_id):
	crop = Crop.objects.get(pk=crop_id)
	CropUnitFormset = inlineformset_factory(Crop, CropUnit, max_num=2, can_delete=True, fields=('unit_type', 'value'))
	if request.method == "POST":
		crop_form = EditCropForm(request.POST, instance=crop, prefix='cropform')
		formset = CropUnitFormset(request.POST, instance=crop, prefix='formset')
		if crop_form.is_valid():
			crop_form.save()
		if formset.is_valid():
			formset.save(commit=False)
			for delete_obj in formset.deleted_objects:
				delete_obj.delete()
			formset.save()
		return HttpResponseRedirect('/crops')
	else:
		crop_form = EditCropForm(instance=crop, prefix='cropform')
		formset = CropUnitFormset(instance=crop, prefix='formset')
	return render(request, 'manager/crop_update_form.html', {'crop_form': crop_form, 'formset': formset})


class InputView(ListView):
	template_name = 'manager/admininput.html'
	context_object_name = 'admininput'
	queryset = InputMethod.objects.all()


class CreateInput(CreateView):
	model = InputMethod
	fields = ['name']
	template_name = 'manager/create_input_form.html'
	success_url = '/inputs'


class UpdateInput(UpdateView):
	model = InputMethod
	fields = ['name']
	template_name_suffix = '_update_form'
	success_url = '/inputs'


class BrandView(ListView):
	template_name = 'manager/adminbrand.html'
	context_object_name = 'adminbrand'
	queryset = Brand.objects.all().extra(select={'case_insensitive_brand': 'lower(name)'}).order_by(
		'case_insensitive_brand')


class DeleteBrand(DeleteView):
	model = Brand
	success_url = reverse_lazy('brands')


class CreateBrand(CreateView):
	form_class = BrandForm
	template_name = 'manager/create_brand_form.html'
	success_url = '/brands'


@login_required
def update_brand(request, brand_id):
	brand = Brand.objects.get(pk=brand_id)
	BrandUnitFormset = inlineformset_factory(Brand, BrandUnit, max_num=2, can_delete=True, fields=('unit', 'value'))
	if request.method == "POST":
		brand_form = BrandForm(request.POST, instance=brand, prefix='brandform')
		formset = BrandUnitFormset(request.POST, instance=brand, prefix='formset')
		if brand_form.is_valid():
			brand_form.save()

		if formset.is_valid():
			formset.save(commit=False)
			for delete_obj in formset.deleted_objects:
				delete_obj.delete()
			formset.save()
		return HttpResponseRedirect('/brands')
	else:
		brand_form = BrandForm(instance=brand, prefix='brandform')
		formset = BrandUnitFormset(instance=brand, prefix='formset')
	return render(request, 'manager/brand_update_form.html', {'brand_form': brand_form, 'formset': formset})


class BrandGroupView(ListView):
	template_name = 'manager/admin_group_brand.html'
	queryset = BrandGroup.objects.all()


@login_required
def get_brandgroups(request):
	groups = BrandGroup.objects.all()
	units = BrandUnit.objects.all()
	return render(request, 'manager/admin_group_brand.html', {'groups': groups, 'units': units})


class CreateBrandGroup(CreateView):
	form_class = BrandGroupForm
	template_name = 'manager/create_brandgroup_form.html'
	success_url = '/brandgroups'


class UpdateBrandGroup(UpdateView):
	model = BrandGroup
	form_class = BrandGroupForm
	template_name_suffix = '_update_form'
	success_url = '/brandgroups'


class DeleteBrandGroup(DeleteView):
	model = BrandGroup
	success_url = reverse_lazy('groupbrands')


class PestView(ListView):
	template_name = 'manager/adminpest.html'
	context_object_name = 'adminpest'
	queryset = Pest.objects.all()


class CreatePest(CreateView):
	model = Pest
	fields = ['name']
	template_name = 'manager/create_pest_form.html'
	success_url = '/pests'


class UpdatePest(UpdateView):
	model = Pest
	fields = ['name']
	template_name_suffix = '_update_form'
	success_url = '/pests'


class CreatePropagation(CreateView):
	form_class = PropagationForm
	template_name = 'manager/create_propagation_form.html'

	def form_valid(self, form):
		obj = form.save(commit=False)
		lot_id = form.cleaned_data['lot']
		lot = Lot.objects.get(lot_id)
		obj.rotation = lot.rotation
		obj.created_by = self.request.user
		obj.save()
		return HttpResponseRedirect('/')


class UpdatePropagation(UpdateView):
	model = Propagation
	form_class = PropagationForm
	template_name_suffix = '_update_form'
	success_url = '/'


@login_required
def create_method(request, lot_name=None):

	MethodFormset = inlineformset_factory(LotInfo, Method, extra=1, can_delete=True, form=MethodForm, fields=(
	'method_name', 'brand', 'quantity', 'time_start_application', 'time_end_application', 'unit', 'people', 'Notes'))
	if request.method == "POST":
		lot_form = LotInfoForm(request.POST, prefix='lotform')
		formset = MethodFormset(request.POST, prefix='formset')
		if lot_form.is_valid():
			formlot = lot_form.save(commit=False)
			lot_id = lot_form.cleaned_data['lot']
			formlot.rotation = lot_id.rotation
			try:
				formlot.crop = lot_id.crop
			except:
				formlot.crop = ''
			formlot.save()

		formset = MethodFormset(request.POST, instance=formlot, prefix='formset')
		if formset.is_valid():
			lot = Lot.objects.get(lot_name=lot_form.cleaned_data['lot'])
			for form in formset.forms:
				obj = form.save(commit=False)
				crops = BrandGroup.objects.filter(brand=obj.brand).values('crops')
				crops = Crop.objects.filter(id__in=crops)
				try:
					if lot.crop in crops:
						obj.created_by = request.user
						obj.save()
					else:
						messages.success(request, "The crop " + str(lot_id.crop) + " is not allowed for the brand " + " " + str(obj.brand))

				except:
					formlot.delete()
					return HttpResponseRedirect('/crop_message')

			return HttpResponseRedirect('/new/method')

	else:
						if lot_name is not None:
								lot_data = Lot.objects.get(lot_name=lot_name)
								lot_form = LotInfoForm(prefix='lotform', initial={'lot': lot_data})
								formset = MethodFormset(prefix='formset')
						else:
								lot_form = LotInfoForm(prefix='lotform')
								formset = MethodFormset(prefix='formset')

	return render(request, 'manager/create_method_form.html', {'lotform': lot_form, 'formset': formset})


class CreateTransplanting(CreateView):
	form_class = TransplantingForm
	template_name = 'manager/create_transplanting_form.html'
	success_url = '/'

	def get_initial(self):
		if self.kwargs:
			lot_object = get_object_or_404(Lot, lot_name=self.kwargs['lot_name'])
			return { 'lot': lot_object }


	def form_valid(self, form):
		obj = form.save(commit=False)
		lot_id = form.cleaned_data['lot']
		lot = Lot.objects.get(pk=lot_id.id)
		lot.crop = form.cleaned_data['crop']
		lot.save()
		obj.rotation = lot_id.rotation
		obj.created_by = self.request.user
		obj.save()
		return HttpResponseRedirect('/')


class UpdateTransplanting(UpdateView):
	model = Transplanting
	form_class = TransplantingForm
	template_name_suffix = '_update_form'
	success_url = '/'


class CreateHarvest(CreateView):
	form_class = HarvestForm
	template_name = 'manager/create_harvest_form.html'
	success_url = '/'

	def get_initial(self):
		if self.kwargs:
			lot_object = get_object_or_404(Lot, lot_name=self.kwargs['lot_name'])
			return { 'lot': lot_object }

	def form_valid(self, form):
		obj = form.save(commit=False)
		lot_id = form.cleaned_data['lot']
		obj.rotation = lot_id.rotation
		try:
			obj.crop = lot_id.crop
		except:
			obj.crop = ''
		obj.created_by = self.request.user
		obj.save()
		return HttpResponseRedirect('/')


class UpdateHarvest(UpdateView):
	model = Harvest
	form_class = HarvestForm
	template_name_suffix = '_update_form'
	success_url = '/'


class CreateCleaning(CreateView):
	form_class = CleaningForm
	template_name = 'manager/create_cleaning_form.html'
	success_url = '/'

	def get_initial(self):
		if self.kwargs:
			lot_object = get_object_or_404(Lot, lot_name=self.kwargs['lot_name'])
			return { 'lot': lot_object }

	def form_valid(self, form):
		obj = form.save(commit=False)
		lot_id = form.cleaned_data['lot']
		lot = Lot.objects.get(pk=lot_id.id)
		obj.rotation = lot.rotation
		lot.rotation += 1
		lot.crop = None
		lot.save()
		try:
			obj.crop = lot_id.crop
		except:
			obj.crop = ''
		obj.created_by = self.request.user
		obj.save()
		return HttpResponseRedirect('/')


class UpdateCleaning(UpdateView):
	model = Cleaning
	form_class = CleaningForm
	template_name_suffix = '_update_form'
	success_url = '/'


@login_required
def get_brands(request):
	inputs = Brand.objects.all()
	return render(request, 'manager/brand_list.html', {'inputs': inputs})


def advanced_history(request):
	if request.method == 'GET':
		lot = Lot.objects.filter(lot_name=request.GET.get('lot').upper())
		lotinfo = LotInfo.objects.filter(lot=lot)
		propagations = Propagation.objects.filter(
			Q(lot__lot_name=request.GET.get('lot').upper()) &
			Q(crop__name__icontains=request.GET.get('crop'))
		).order_by('-created')

		if request.GET.get('crop') is not None:
			inputs = Method.objects.filter(lot_info__in =lotinfo).order_by('-created')
		else:
			inputs = Method.objects.filter(lot_info__in=lotinfo,
			                               lot_info__crop__icontains=request.GET.get('crop')).order_by('-created')
		transplantings = Transplanting.objects.filter(
			Q(lot__lot_name=request.GET.get('lot').upper()) &
			Q(crop__name__icontains=request.GET.get('crop'))
		).order_by('-created')
		harvests = Harvest.objects.filter(
			Q(lot__lot_name=request.GET.get('lot').upper()) &
			Q(crop__icontains=request.GET.get('crop'))
		).order_by('-created')
		cleanings = Cleaning.objects.filter(
			Q(lot__lot_name=request.GET.get('lot').upper()) &
			Q(crop__icontains=request.GET.get('crop'))
		).order_by('-created')

		units = BrandUnit.objects.all()
		crop_units = CropUnit.objects.all()
		show_fields = HistorySettings.objects.filter(field_view=False).only('field_name')
		fields = [str(f) for f in show_fields]
		page = request.GET.get('page', 1)
		hist = list(
			sorted(
				chain(inputs, transplantings, harvests, cleanings),
				key=lambda objects: objects.created,
				reverse=True
			))
		paginator = Paginator(hist, 300)
		try:
			histories = paginator.page(page)
		except PageNotAnInteger:
			histories = paginator.page(1)
		except EmptyPage:
			histories = paginator.page(paginator.num_pages)
		return render(request, 'manager/advance_search.html',
						{'histories': histories, 'units': units, 'crops': crop_units, 'fields': fields})


@login_required
def get_history(request):
	propagations = Propagation.objects.all().order_by('-created')
	if 'history' in request.build_absolute_uri():
		inputs = Method.objects.all().order_by('-created')
	else:
		inputs = Method.objects.filter(created__gte=datetime.datetime.now() - datetime.timedelta(days = 730)).order_by('-created')
	transplantings = Transplanting.objects.all().order_by('-created')
	harvests = Harvest.objects.all().order_by('-created')
	cleanings = Cleaning.objects.all()
	units = BrandUnit.objects.all()
	crop_units = CropUnit.objects.all()
	brandgroup = BrandGroup.objects.all()
	show_fields = HistorySettings.objects.filter(field_view=False).only('field_name')
	fields = [str(f) for f in show_fields]
	page = request.GET.get('page', 1)
	hist = list(
		sorted(
			chain(inputs, transplantings, harvests, cleanings),
			key=lambda objects: objects.created,
			reverse=True
		))
	paginator = Paginator(hist, 200)
	try:
		histories = paginator.page(page)
	except PageNotAnInteger:
		histories = paginator.page(1)
	except EmptyPage:
		histories = paginator.page(paginator.num_pages)
	if 'history' in request.build_absolute_uri():
		return render(request, 'manager/history_list.html',
					{'histories': histories, 'units': units, 'crops': crop_units, 'fields': fields})
	else:
		return render(request, 'manager/history_wps.html',
						{'histories': histories, 'units': units, 'crops': crop_units, 'fields': fields, 'brandgroup':brandgroup})

@login_required
def get_rup_history(request):
	inputs = Method.objects.filter(brand__rup_omri='RUP').filter(created__range=["2020-01-01", "2021-01-01"]).order_by('-created')
	units = BrandUnit.objects.all()
	crop_units = CropUnit.objects.all()
	brandgroup = BrandGroup.objects.all()

	page = request.GET.get('page', 1)
	hist = list(
		sorted(
			chain(inputs),
			key=lambda objects: objects.created,
			reverse=True
		))
	paginator = Paginator(hist, 1000)
	try:
		histories = paginator.page(page)
	except PageNotAnInteger:
		histories = paginator.page(1)
	except EmptyPage:
		histories = paginator.page(paginator.num_pages)
	return render(request, 'manager/history_rup.html',
					{'histories': histories, 'units': units, 'crops': crop_units, 'brandgroup': brandgroup})


@login_required
def load_json_data(request):
	json_list = os.listdir(settings.BASE_DIR + '/static/kml/')
	status=[]
	for k in json_list:
		lot = k.replace('.kml','').upper()
		status2 = lot_status_map(lot)
		status.append(status2)
	return render(request, 'manager/map.html', {'json_list': json_list, 'status': status})


def lot_activities(field, is_field=True):
	jsondata = []
	try:
		if is_field:
			lot = Lot.objects.get(lot_name=field)
			lotinfo = LotInfo.objects.filter(lot=lot)
			if lot.crop=='None':
				item = {"id": 0}
				item['name'] = 'No data available'
				item['crop'] = ''
				item['created'] = ''
				jsondata.append(item)
				return (jsondata)
		else:
			lot = Lot.objects.get(pk=field)
			lotinfo = LotInfo.objects.filter(lot=lot)
			if lot.crop=='None':
				item = {"id": 0}
				item['name'] = 'No data available'
				item['crop'] = ''
				item['created'] = ''
				jsondata.append(item)
				return (jsondata)
	except:
		item = {"id": 0}
		item['name'] = 'No data available'
		item['crop'] = ''
		item['created'] = ''
		jsondata.append(item)
		return (jsondata)

	try:
		propagations = Propagation.objects.filter(lot=lot)
	except:
		propagations = ''
	try:
		inputs = Method.objects.filter(lot_info__in=lotinfo)
	except:
		inputs = ''
	try:
		transplantings = Transplanting.objects.filter(lot=lot)
	except:
		transplantings = ''
	try:
		harvests = Harvest.objects.filter(lot=lot)
	except:
		harvests = ''
	try:
		cleanings = Cleaning.objects.filter(lot=lot)
	except:
		cleanings = ''
	hist = list(
		sorted(
			chain(propagations, inputs, transplantings, harvests, cleanings),
			key=lambda objects: objects.created,
			reverse=True
		))
	status, method_status = lot_status(lot.lot_name)
	for h in hist[:5]:
		if status:
			item = {"id": h.pk, "phi": status['phi'], "rei": status['rei'], "date_rei": status["date_rei"],
					"date_phi": status["date_phi"]}
		else:
			item = {"id": h.pk, "phi": 0, "rei": 0}
		if h.__class__.__name__ == 'Method':
			method_rei, method_phi = get_method_status(h)
			item['lot'] = h.lot_info.lot.lot_name
			item['lot_crop'] = h.lot_info.crop
			item['lot_rotation'] = h.lot_info.lot.rotation
			item['name'] = h.method_name.name
			item['info'] = h.brand.name + '/' + str(h.quantity) + '/' + h.get_unit_display()
			item['created'] = h.created.strftime('%m-%d')
			item["method_rei"]=method_rei
			item["method_phi"] = method_phi

		elif h.__class__.__name__ == 'Harvest':
			item['lot'] = h.lot.lot_name
			try:
				item['lot_crop'] = h.lot.crop.name
			except:
				item['lot_crop'] = ''
			item['lot_rotation'] = h.lot.rotation
			item['name'] = h.__class__.__name__
			item['info'] = str(h.quantity)
			item['created'] = h.created.strftime('%m-%d')

		elif h.__class__.__name__ == 'Transplanting':
			item['lot'] = h.lot.lot_name
			try:
				item['lot_crop'] = h.lot.crop.name
			except:
				item['lot_crop'] = ''
			item['lot_rotation'] = h.lot.rotation
			item['name'] = h.__class__.__name__
			item['info'] = str(h.quantity)
			item['created'] = h.created.strftime('%m-%d')

		elif h.__class__.__name__ == 'Cleaning':
			item['lot'] = h.lot.lot_name
			try:
				item['lot_crop'] = h.lot.crop.name
			except:
				item['lot_crop'] = ''
			item['lot_rotation'] = h.lot.rotation
			item['name'] = h.__class__.__name__
			item['info'] = h.get_action_display()
			item['created'] = h.created.strftime('%m-%d')

		elif h.__class__.__name__ == 'Propagation':
			item['lot'] = h.lot.lot_name
			try:
				item['lot_crop'] = h.lot.crop.name
			except:
				item['lot_crop'] = ''
			item['lot_rotation'] = h.lot.rotation
			item['name'] = h.__class__.__name__
			item['info'] = str(h.quantity)
			item['created'] = h.created.strftime('%m-%d')
		jsondata.append(item)
	return (jsondata)


def get_method_status(input):
	try:
		brandgroup = BrandGroup.objects.get(brand= input.brand, crops__in=[input.lot_info.lot.crop])
	except:
		rei=0
		phi=0
		return(rei, phi)

	if brandgroup.rei_time == 'h':
		if ((input.created.replace(hour=input.time_end_application.hour,
																		minute=input.time_end_application.minute) + datetime.timedelta(
			hours=int(brandgroup.rei)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
			rei = 1
		else:
			rei = 0
	else:
		if ((input.created.replace(hour=input.time_end_application.hour,
																		minute=input.time_end_application.minute) + datetime.timedelta(
			hours=int(brandgroup.rei) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
			rei = 1
		else:
			rei = 0
	if brandgroup.phi_time == 'h':
		if ((input.created.replace(hour=input.time_end_application.hour,
																		minute=input.time_end_application.minute) + datetime.timedelta(
			hours=int(brandgroup.phi)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
			phi = 1
		else:
			phi = 0
	else:
		if ((input.created.replace(hour=input.time_end_application.hour,
																		minute=input.time_end_application.minute) + datetime.timedelta(
			hours=int(brandgroup.phi) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
			phi = 1

		else:
			phi= 0
	return (rei, phi)


# Function that gets the info for each field and gets passed to the view
def lot_status(field):
	lista = []
	lotstatus = {}
	statuses = {}
	try:
		lot = Lot.objects.get(lot_name=field)
		lotinfo = LotInfo.objects.filter(lot=lot)

		if lot.crop==None:
			return ('','')
	except:
		return ('')
	try:
		last_cleaning = Cleaning.objects.filter(lot=lot).order_by('-id')[0]
		last_method = Method.objects.filter(lot_info__in=lotinfo).order_by('-id')[0]
		last_harvest = Harvest.objects.filter(lot=lot).order_by('-id')[0]
		last_transplanting = Transplanting.objects.filter(lot=lot).order_by('-id')[0]
	except:
		print "no last"
	try:
		list_inputs = Method.objects.filter(lot_info__in=lotinfo).filter(
			created__gte=datetime.datetime.now() - datetime.timedelta(days=5))

		for last_input in list_inputs:
			status = {}
			try:
				brandgroup = BrandGroup.objects.get(brand=last_input.brand, crops__in=[lot.crop])
			except:
				continue
			if brandgroup.rei_time == 'h':
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['rei'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei)) - datetime.datetime.now()
					status['date_rei'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['rei'] = 0
					status['date_rei'] = ''
					lista.append(status)
			else:
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['rei'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei) * 24) - datetime.datetime.now()
					status['date_rei'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['rei'] = 0
					status['date_rei'] = ''
					lista.append(status)
			if brandgroup.phi_time == 'h':
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['phi'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi)) - datetime.datetime.now()
					status['date_phi'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['phi'] = 0
					status['date_phi'] = ''
					lista.append(status)
			else:
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['phi'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi) * 24) - datetime.datetime.now()
					status['date_phi'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['phi'] = 0
					status['date_phi'] = ''
					lista.append(status)
		phi_date = [x['date_phi'] for x in lista if isinstance(x['date_phi'], datetime.datetime)]
		if phi_date:
			phi_date = max(phi_date).strftime('%m-%d %H:%M')
		else:
			phi_date = ''
		rei_date = [x['date_rei'] for x in lista if isinstance(x['date_rei'], datetime.datetime)]
		if rei_date:
			rei_date = max(rei_date).strftime('%m-%d %H:%M')
		else:
			rei_date = ''
		rei = [x['rei'] for x in lista]
		phi = [x['phi'] for x in lista]
		try:
			if (last_cleaning.created > last_method.created) and (last_cleaning.created > last_harvest.created) \
				and (last_cleaning.created > last_transplanting.created):
				lotstatus = {'rei': 0, 'date_rei': 0, 'phi': 0, 'date_phi': 0, 'cleaning':1}
				statuses = {'rei': rei, 'phi': phi}

			else:
				lotstatus = {'rei': max(rei), 'date_rei': rei_date, 'phi': max(phi), 'date_phi': phi_date}
				statuses = {'rei': rei, 'phi': phi}
		except:
			lotstatus = {'rei': max(rei), 'date_rei': rei_date, 'phi': max(phi), 'date_phi': phi_date}
			statuses = {'rei': rei, 'phi': phi}
	except:
		print 'no data available'
	return (lotstatus, statuses)


def lot_status_map(field):
	lista = []
	lotstatus = {}
	statuses = {}
	try:
		lot = Lot.objects.get(lot_name=field)
		lotinfo = LotInfo.objects.filter(lot=lot)

		if lot.crop==None:
			lotstatus = {'rei': 3, 'date_rei': 0, 'phi': 0, 'date_phi': 0}
			return (lotstatus)
	except:
		return ('')
	try:
		if Cleaning.objects.filter(lot=lot).exists():
			last_cleaning = Cleaning.objects.filter(lot=lot).order_by('-id')[0]
		else:
			last_cleaning=None
			print "No cleaning"
		if Method.objects.filter(lot_info__in=lotinfo).exists():
			last_method = Method.objects.filter(lot_info__in=lotinfo).order_by('-id')[0]
		else:
			print "No input"
		if Harvest.objects.filter(lot=lot).exists():
			last_harvest = Harvest.objects.filter(lot=lot).order_by('-id')[0]
		else:
			print "No Harvest"
		if Transplanting.objects.filter(lot=lot).exists():
			last_transplanting = Transplanting.objects.filter(lot=lot).order_by('-id')[0]
		else:
			print "no transplanting"
	except:
		print "no last"
	try:
		list_inputs = Method.objects.filter(lot_info__in=lotinfo).filter(
			created__gte=datetime.datetime.now() - datetime.timedelta(days=5))

		for last_input in list_inputs:
			status = {}
			try:
				brandgroup = BrandGroup.objects.get(brand=last_input.brand, crops__in=[lot.crop])
			except:
				continue
			if brandgroup.rei_time == 'h':
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['rei'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei)) - datetime.datetime.now()
					status['date_rei'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['rei'] = 0
					status['date_rei'] = ''
					lista.append(status)
			else:
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['rei'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.rei) * 24) - datetime.datetime.now()
					status['date_rei'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['rei'] = 0
					status['date_rei'] = ''
					lista.append(status)
			if brandgroup.phi_time == 'h':
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi)) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['phi'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi)) - datetime.datetime.now()
					status['date_phi'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['phi'] = 0
					status['date_phi'] = ''
					lista.append(status)
			else:
				if ((last_input.created.replace(hour=last_input.time_end_application.hour,
												minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi) * 24) - datetime.datetime.now()) > datetime.timedelta(hours=0)):
					status['phi'] = 1
					date_time = last_input.created.replace(hour=last_input.time_end_application.hour,
															 minute=last_input.time_end_application.minute) + datetime.timedelta(
						hours=int(brandgroup.phi) * 24) - datetime.datetime.now()
					status['date_phi'] = date_time + datetime.datetime.now()
					lista.append(status)
				else:
					status['phi'] = 0
					status['date_phi'] = ''
					lista.append(status)
		phi_date = [x['date_phi'] for x in lista if isinstance(x['date_phi'], datetime.datetime)]
		if phi_date:
			phi_date = max(phi_date).strftime('%m-%d %H:%M')
		else:
			phi_date = ''
		rei_date = [x['date_rei'] for x in lista if isinstance(x['date_rei'], datetime.datetime)]
		if rei_date:
			rei_date = max(rei_date).strftime('%m-%d %H:%M')
		else:
			rei_date = ''
		rei = [x['rei'] for x in lista]
		phi = [x['phi'] for x in lista]
		try:
			if Cleaning.objects.filter(lot=lot).exists():
				if rei_date =='' and (last_cleaning.created > last_harvest.created) \
					and (last_cleaning.created > last_transplanting.created):
					lotstatus = {'rei': 0, 'date_rei': 0, 'phi': 0, 'date_phi': 0, 'cleaning':1}
				elif rei_date =='' and (last_harvest.created > last_cleaning.created) \
					and (last_harvest.created > last_transplanting.created):
					lotstatus = {'rei': 0, 'date_rei': 0, 'phi': 0, 'date_phi': 0, 'cleaning':0}
				else:
					lotstatus = {'rei': max(rei), 'date_rei': rei_date, 'phi': max(phi), 'date_phi': phi_date}
			else:
				if rei_date =='' and (last_harvest.created > last_transplanting.created):
					lotstatus = {'rei': 0, 'date_rei': 0, 'phi': 0, 'date_phi': 0, 'cleaning': 0}
				else:
					lotstatus = {'rei': max(rei), 'date_rei': rei_date, 'phi': max(phi), 'date_phi': phi_date}
		except:
			lotstatus = {'rei': max(rei), 'date_rei': rei_date, 'phi': max(phi), 'date_phi': phi_date}
	except:
		print 'no data available'
	return (lotstatus)


@login_required
def get_lot_activities(request):
	lots = get_lots()
	lot_activ = []
	for l in lots:
		activities = lot_activities(l, is_field=True)
		if activities:
			lot_activ.append(activities)
	return render(request, 'manager/home.html', {'lots': lot_activ})


def get_lot_status(request, field):
	status,_ = lot_status(field)
	return HttpResponse(json.dumps(status), content_type="application/json")


def get_json_lot_activities(request, field):
	activities = lot_activities\
		(field)
	return HttpResponse(json.dumps(activities), content_type="application/json")


class SettingsView(ListView):
	template_name = 'manager/settings.html'
	queryset = HistorySettings.objects.all()


class UpdateSettings(UpdateView):
	model = HistorySettings
	fields = ['field_name', 'field_view']
	template_name_suffix = '_update_form'
	success_url = '/settings'


def get_lots():
	propagations = Propagation.objects.order_by('-created')[:100]
	inputs = Method.objects.order_by('-created')[:300]
	transplantings = Transplanting.objects.order_by('-created')[:200]
	harvests = Harvest.objects.order_by('-created')[:200]
	cleanings = Cleaning.objects.order_by('-created')[:200]
	activities= list(
		sorted(
			chain(inputs, transplantings, harvests, cleanings),
			key=lambda objects: objects.created,
			reverse=True
		))
	result=[]
	for act in activities:
		if act.__class__.__name__== 'Method':
			lot= act.lot_info.lot.lot_name
			if lot not in result:
				result.append(lot)
		else:
			lot = act.lot.lot_name
			if lot not in result:
				result.append(lot)
	return result
