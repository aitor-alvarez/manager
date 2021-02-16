from django.db import models
from datetime import datetime

cropunit_choices=(
('Propagation', 'Propagation/Planting Unit'), 
('Harvest','Harvest Unit'),
)

rup_choices=(
('RUP', 'RUP'), 
('OMRI','OMRI'),
)

brand_unit_choices=(
	('F', 'Field Unit'),
	('P', 'Purchase Unit'),
	)

time_choices=(
	('d', 'Days'),
	('h', 'Hours'),
	)

method_units=(
('G', 'Gal'),
('O', 'Oz'),
('Q', 'Quart'),
('P', 'Pint'),
('L', 'Lbs'),
	)

cleaning_choices=(
('F', 'Full Cleaning'), 
('H','Half Cleaning'),
	)


class Lot(models.Model):
	lot_name = models.CharField(max_length=100)
	rotation = models.IntegerField(blank=True)
	crop = models.ForeignKey('Crop', null=True, blank=True, default=None)
	acres = models.FloatField(null=True, blank=True, default=None)
	tax_code = models.CharField(max_length=100, null=True, blank=True, default=None)
	county = models.CharField(max_length=100, null=True, blank=True, default=None)
	class Meta:
		ordering = ['lot_name']

	def __unicode__(self):
		return self.lot_name

class Crop(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['name']
	def __unicode__(self):
		return self.name

class CropUnit(models.Model):
	crop = models.ForeignKey('Crop')
	unit_type = models.CharField(choices=cropunit_choices, max_length=12, blank=True)
	value = models.CharField(max_length=100, default=None, blank=True)
	def __unicode__(self):
		return self.unit_type+" "+self.value

class InputMethod(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

class Brand(models.Model):
	name = models.CharField(max_length=100)
	epa_number = models.CharField(max_length=100, default=None, blank=True)
	active_ingredient = models.CharField(max_length=100, blank=True)
	type_of_formulation = models.CharField(max_length=100, blank=True)
	physical_state = models.CharField(max_length=100, blank=True)
	rup_omri = models.CharField(choices= rup_choices, max_length=4, blank=True)
	pests = models.ManyToManyField('Pest', blank=True)
	class Meta:
		ordering = ['name']
	def __unicode__(self):
		return self.name

class BrandGroup(models.Model):
	brand = models.ForeignKey('Brand')
	crops = models.ManyToManyField('Crop')
	rei = models.CharField(max_length=100, blank=True)
	rei_time = models.CharField(choices=time_choices, max_length=1)
	phi = models.CharField(max_length=100, blank=True)
	phi_time = models.CharField(choices=time_choices, max_length=1)
	rate = models.CharField(max_length=100, blank=True, null=True)
	def __unicode__(self):
		return self.brand.name

class BrandUnit(models.Model):
	brand = models.ForeignKey('Brand')
	unit = models.CharField(choices=brand_unit_choices, max_length=1)
	value = models.CharField(max_length=100, blank=True, null=True)
	unit_cost = models.FloatField(blank=True, null=True)
	def __unicode__(self):
		return self.get_unit_display()+' '+str(self.unit_cost)

class Pest(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name


class Propagation(models.Model):
	rotation = models.IntegerField(blank=True)
	crop = models.ForeignKey('Crop')
	lot = models.ForeignKey('Lot')
	quantity = models.FloatField(null=True, blank=True, default=None)
	quantity_unit = models.CharField(max_length=100, blank=True)
	people = models.IntegerField(blank=True)
	Notes = models.TextField(blank=True)
	created_by = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)

	def __unicode__(self):
		return str(self.lot)


class LotInfo(models.Model):
	lot = models.ForeignKey('Lot')
	rotation = models.IntegerField(blank=True)
	crop = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return str(self.lot)


class Method(models.Model):
	lot_info = models.ForeignKey('LotInfo')
	method_name = models.ForeignKey('InputMethod')
	brand = models.ForeignKey('Brand')
	quantity = models.FloatField(null=True, blank=True, default=None)
	unit = models.CharField(max_length=2, choices=method_units, blank=True)
	people = models.IntegerField(blank=True)
	Notes = models.TextField(blank=True)
	time_start_application = models.TimeField(default='00:00')
	time_end_application = models.TimeField(default='00:00')
	created_by = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)
	def __unicode__(self):
		return str(self.lot_info.lot.lot_name)+' '+str(self.method_name.name)


class Transplanting(models.Model):
	lot = models.ForeignKey('Lot')
	crop = models.ForeignKey('Crop')
	rotation = models.IntegerField(blank=True)
	quantity = models.FloatField(null=True, blank=True, default=None)
	quantity_description = models.CharField(max_length=100, blank=True)
	people = models.IntegerField(blank=True)
	Notes = models.TextField(blank=True)
	created_by = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)

	def __unicode__(self):
		return str(self.lot)


class Harvest(models.Model):
	lot = models.ForeignKey('Lot')
	rotation = models.IntegerField(blank=True)
	crop = models.CharField(max_length=100, blank=True)
	quantity = models.IntegerField(blank=True)
	people = models.IntegerField(blank=True)
	Notes = models.TextField(blank=True)
	created_by = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)

	def __unicode__(self):
		return str(self.lot)


class Cleaning(models.Model):
	lot = models.ForeignKey('Lot')
	rotation = models.IntegerField(blank=True)
	crop = models.CharField(max_length=100, blank=True)
	action = models.CharField(choices=cleaning_choices, max_length=1)
	people = models.IntegerField(blank=True, null=True)
	Notes = models.TextField(blank=True)
	created_by = models.CharField(max_length=50, blank=True)
	created = models.DateTimeField(default=datetime.now, blank=True)

	def __unicode__(self):
		return str(self.lot)


class ItemShow(models.Model):
	field = models.CharField(max_length=150)
	def __unicode__(self):
		return str(self.field)


class HistorySettings(models.Model):
	field_name = models.OneToOneField(
        ItemShow,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	field_view =models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.field_name)
