# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView
from .models import Item, Service
from django.shortcuts import render
from .forms import ItemForm, EditItemForm, ServiceForm
from django.shortcuts import get_object_or_404, redirect, render, reverse
from datetime import date
import datetime


class CreateItem(CreateView):
		form_class = ItemForm
		model = Item
		template_name = 'inventory/create_item.html'
		success_url = '/items'

		def form_valid(self, form):
				type = form.cleaned_data['type']
				make = form.cleaned_data['make']
				category = form.cleaned_data['category']
				description = form.cleaned_data['description']
				data = form.save(commit=False)
				if category == 'T':
					data.code = 'Trap'+'_'+type[:3]+'_'+description[:3]
					data.save()
				elif category == 'T':
					data.code = type[:3] + '_' + make[:3] + '_' + description[:3]
					data.save()


				return super(CreateItem, self).form_valid(form)


class CreateService(CreateView):
		form_class = ServiceForm
		model = Service
		template_name = 'inventory/create_service.html'


		def form_valid(self, form):
				item = Item.objects.get(pk=self.kwargs['item_id'])
				form.instance.vehicle = item
				return super(CreateService, self).form_valid(form)

		def get_context_data(self, **kwargs):
				context = super(CreateService, self).get_context_data(**kwargs)
				vehicle_id = self.kwargs['item_id']
				context['vehicle'] = Item.objects.get(pk=vehicle_id)
				return context

		def get_success_url(self):
			return '/items/view/'+self.kwargs['item_id']


class ItemView(ListView):
		model = Item
		template_name = 'inventory/item_list.html'


def show_items(request):
	items = Item.objects.all()
	output_list = []
	for it in items:
		output={'id':it.pk, 'code':it.code, 'type':it.type, 'description': it.description, 'check':  next_check(it)}
		output_list.append(output)
	return render(request, 'inventory/item_list.html', {'item_list': output_list})


def next_check(item):
	try:
		last_service = Service.objects.filter(vehicle=item)[0]
		if last_service.service_date:
			limit = last_service.service_date + datetime.timedelta(days=int(item.next_check_in_days))
			if date.today() >= limit:
				return True
			else:
				return False
	except:
		return False


class ServiceView(ListView):
		model = Item
		queryset = Service.objects.all().order_by('-service_date')
		template_name = 'inventory/services.html'


def update_item(request, item_id):
		instance = get_object_or_404(Item, id=item_id)
		form = EditItemForm(request.POST or None, instance=instance)
		if form.is_valid():
				type = form.cleaned_data['type']
				make = form.cleaned_data['make']
				description = form.cleaned_data['description']
				data = form.save(commit=False)
				data.code = type[:3] + '_' + make[:3] + '_' + description[:3]
				data.save()
				return redirect('view_items')
		return render(request, 'inventory/update_item.html', {'form': form})


def update_service(request, service_id):
		instance = get_object_or_404(Service, id=service_id)
		form = ServiceForm(request.POST or None, instance=instance)
		if form.is_valid():
				form.save()
				return redirect(reverse('view_item', kwargs={'item_id': instance.vehicle_id}))
		return render(request, 'inventory/update_service.html', {'form': form})


def show_item(request, item_id):
		item = Item.objects.get(id=item_id)
		services = Service.objects.filter(vehicle=item).order_by('-id')
		return render(request, 'inventory/detail.html', {'item':item, 'services': services})


class SearchView(ListView):
	model = Item
	template_name = 'inventory/item_search.html'

