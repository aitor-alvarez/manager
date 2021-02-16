from .models import *
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'email': forms.HiddenInput(),

        }


class LotChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return str(obj.lot_name)+' ('+str(obj.rotation)+') '+str(obj.crop)


class EditCropForm(forms.ModelForm):
	class Meta:
		model=Crop
		fields = ['name']
		widgets = {
		'name' : forms.TextInput(attrs={'class':'form-control', 'required': 'true'}),

		}


class BrandForm(forms.ModelForm):
	class Meta:
		model=Brand
		fields = ['name', 'epa_number', 'active_ingredient', 'rup_omri', 'pests']
		widgets={
		'name' : forms.TextInput(attrs={'class':'form-control', 'required': 'true'}),
		'epa_number' : forms.TextInput(attrs={'class':'form-control'}),
		'active_ingredient' : forms.TextInput(attrs={'class':'form-control'}),
		'rup_omri' : forms.Select(attrs={'class':'form-control'}),
		'pests' : forms.CheckboxSelectMultiple(),
		}



class BrandGroupForm(forms.ModelForm):
	class Meta:
		model=BrandGroup
		fields = ['brand', 'crops', 'rei', 'rei_time','phi', 'phi_time','rate']
		widgets={
		'brand' : forms.Select(attrs={'class':'form-control', 'required': 'true'}),
		'crops' : forms.CheckboxSelectMultiple(),
		'rei' : forms.TextInput(attrs={'class':'form-control'}),
		'rei_time' : forms.Select(attrs={'class':'form-control', 'required': 'true'}),
		'phi' : forms.TextInput(attrs={'class':'form-control'}),
		'phi_time' : forms.Select(attrs={'class':'form-control', 'required': 'true'}),
		'rate' : forms.TextInput(attrs={'class':'form-control'}),
		}


class PropagationForm(forms.ModelForm):
	class Meta:
		model=Propagation
		fields = ['crop', 'lot', 'quantity', 'quantity_unit','people', 'Notes', 'rotation']
		widgets={
		'crop': forms.Select(attrs={'class':'form-control'}),
		'lot' : forms.Select(attrs={'class':'form-control'}),
		'rotation' : forms.HiddenInput(),
		'quantity' : forms.NumberInput(attrs={'class':'form-control'}),
		'quantity_unit' : forms.TextInput(attrs={'class':'form-control'}),
		'people' : forms.NumberInput(attrs={'class':'form-control'}),
		'Notes' : forms.Textarea(attrs={'class':'form-control'}),
		}


class LotInfoForm(forms.ModelForm):
	lot = LotChoiceField(queryset=Lot.objects.all(), required = True)
	class Meta:
		model = LotInfo
		
		fields = ['lot', 'rotation', 'crop']
		widgets={
			'lot': forms.Select(attrs={'class':'form-control'}),
			'rotation': forms.HiddenInput(),
			'crop' : forms.HiddenInput(),
			}

class MethodForm(forms.ModelForm):
	class Meta:
		model=Method
		fields = ['lot_info','method_name', 'brand','quantity', 'time_start_application', 'time_end_application', 'unit' ,'people', 'Notes', 'created_by']
		widgets={
		'lot_info' : forms.HiddenInput(),
		'created_by' : forms.HiddenInput(),
		'method_name': forms.Select(attrs={'class':'form-control'}),
		'brand': forms.Select(attrs={'class':'form-control'}),
		'quantity' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'time_start_application': forms.TimeInput(format='%H:%M'),
		'time_end_application': forms.TimeInput(format='%H:%M'),
		'unit' : forms.Select(attrs={'class':'form-control', 'required': 'true'}),
		'people' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'Notes' : forms.Textarea(attrs={'class':'form-control'}),
		}


class TransplantingForm(forms.ModelForm):
	class Meta:
		model=Transplanting
		fields = ['lot', 'crop','quantity', 'people', 'Notes', 'rotation', 'crop']
		widgets={
		'lot' : forms.Select(attrs={'class':'form-control'}),
		'crop' : forms.Select(attrs={'class':'form-control'}),
		'quantity' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'rotation' : forms.HiddenInput(),
		'people' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'Notes' : forms.Textarea(attrs={'class':'form-control'}),
		}

	
class HarvestForm(forms.ModelForm):
	lot = LotChoiceField(queryset=Lot.objects.all(), required=True)
	class Meta:
		model=Harvest
		fields = ['lot', 'quantity', 'people', 'Notes', 'rotation', 'crop']
		widgets={
		'lot' : forms.Select(attrs={'class':'form-control'}),
		'rotation' : forms.HiddenInput(),
		'crop' : forms.HiddenInput(),
		'quantity' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'people' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'Notes' : forms.Textarea(attrs={'class':'form-control'}),
		}


class CleaningForm(forms.ModelForm):
	class Meta:
		model=Cleaning
		fields = ['lot', 'action', 'people', 'Notes', 'rotation', 'crop']
		widgets={
		'lot' : forms.Select(attrs={'class':'form-control'}),
		'rotation' : forms.HiddenInput(),
		'crop' : forms.HiddenInput(),
		'action' : forms.Select(attrs={'class':'form-control'}),
		'people' : forms.NumberInput(attrs={'class':'form-control', 'required': 'true'}),
		'Notes' : forms.Textarea(attrs={'class':'form-control'}),
		}	


