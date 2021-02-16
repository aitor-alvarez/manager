from django import forms
from planner.models import *
from manager.models import Lot, Crop


class PlanForm(forms.ModelForm):
	field = forms.ModelChoiceField(queryset= Lot.objects.order_by('lot_name'), widget=forms.Select(attrs={'class':'form-control', 'required': 'true'}))
	crop = forms.ModelChoiceField(queryset = Crop.objects.order_by('name'), widget=forms.Select(attrs={'class':'form-control', 'required': 'true'}))
	class Meta:
		model=Plan
		fields = ('field', 'crop', 'start_date',)
		widgets={
		'start_date' : forms.DateInput(attrs={'class':'form-control', 'required': 'true'}),
		}

class PlanPartForm(forms.ModelForm):
	class Meta:
		model=PlanPart
		fields = ['plan','plan_type']
		widgets={
		'plan' : forms.HiddenInput(),
		'event' : forms.HiddenInput(),
		'plan_type' : forms.Select(attrs={'class':'form-control'}),
		

		}

class CalendarForm(forms.ModelForm):
	class Meta:
		model=Plan
		fields = ['field', 'crop']
		widgets={
		'field' : forms.Select(attrs={'class':'form-control'}),
		'crop' : forms.Select(attrs={'class':'form-control'}),
		}


        
