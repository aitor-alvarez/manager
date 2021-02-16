from .models import *
from django import forms
from datetime import datetime, date, timedelta

category_choices = (

		('T', 'Trap'),
('V', 'Vehicle'),
('N','Non Registered (Tractor, Farm Uses)'),
	)

class EditItemForm(forms.ModelForm):
	DAYS = (
		(15, 'Every two weeks'),
		(30, 'Once a month'),
		(60, 'Bimonthly'),
		(90, 'Quarterly'),
		(183, 'Twice a year'),
		(365, 'Yearly'),
	)

	#category = forms.ChoiceField(choices=category_choices, required=True)
	next_check_in_days = forms.ChoiceField(choices=DAYS, required=True)
	safety_expires = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day")
		),
	)
	insurance_expires = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),
	)
	registration_expires = forms.DateField(initial=date.today(),
	                                       widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),)

	class Meta:
		model=Item
		exclude = ('created', 'plate')
		widgets = {
			'category': forms.Select(attrs={'class': 'form-control'}),
			'next_check_in_days': forms.Select(attrs={'class': 'form-control'}),
			'type': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.TextInput(attrs={'class': 'form-control'}),
			'location': forms.TextInput(attrs={'class': 'form-control'}),
			'code': forms.HiddenInput(),
			'notes': forms.Textarea(attrs={'class': 'form-control'}),
			'license': forms.TextInput(attrs={'class': 'form-control'}),
			'make': forms.TextInput(attrs={'class': 'form-control'}),
			'model': forms.TextInput(attrs={'class': 'form-control'}),
			'vin_serial': forms.TextInput(attrs={'class': 'form-control'}),
			'year': forms.TextInput(attrs={'class': 'form-control'}),
			'insurance': forms.TextInput(attrs={'class': 'form-control'}),
			'insurance_expires': forms.TextInput(attrs={'class': 'form-control'}),
			'safety_expires': forms.TextInput(attrs={'class': 'form-control'}),
			'registration_expires': forms.TextInput(attrs={'class': 'form-control'}),
			'registration_amount': forms.TextInput(attrs={'class': 'form-control'}),
			'tire_front': forms.TextInput(attrs={'class': 'form-control'}),
			'tire_back': forms.TextInput(attrs={'class': 'form-control'}),
			'tare': forms.TextInput(attrs={'class': 'form-control'}),

		}


class ItemForm(forms.ModelForm):
	DAYS = (
		(15, 'Every two weeks'),
		(30, 'Once a month'),
		(45, 'Bimonthly'),
		(90, 'Quarterly'),
		(183, 'Twice a year'),
		(365, 'Yearly'),
	)

	category = forms.ChoiceField(choices=category_choices, required=True)
	next_check_in_days = forms.ChoiceField(choices=DAYS, required=True)
	safety_expires = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),
	)
	insurance_expires = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),
	)
	registration_expires = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),
	)
	class Meta:
		model = Item
		exclude =('created', 'plate')
		widgets = {
						'category': forms.Select(attrs={'class': 'form-control'}),
						'next_check_in_days': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
						'description': forms.TextInput(attrs={'class': 'form-control'}),
						'location': forms.TextInput(attrs={'class': 'form-control'}),
			      'code': forms.HiddenInput(),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'license': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
						'model': forms.TextInput(attrs={'class': 'form-control'}),
            'vin_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'safety_expires': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_expires': forms.TextInput(attrs={'class': 'form-control'}),
            'safety_expires': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_expires': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_amount': forms.TextInput(attrs={'class': 'form-control'}),
            'tire_front': forms.TextInput(attrs={'class': 'form-control'}),
            'tire_back': forms.TextInput(attrs={'class': 'form-control'}),
            'tare': forms.TextInput(attrs={'class': 'form-control'}),

		}

class ServiceForm(forms.ModelForm):
    service_date = forms.DateField(initial=date.today(),
		widget=forms.SelectDateWidget(
			empty_label=("Choose Year", "Choose Month", "Choose Day"),
		),
	)

    class Meta:
        model = Service
        exclude =('created','vehicle')
        widgets = {
			'service_date': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
		}

