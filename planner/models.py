from __future__ import unicode_literals
import datetime
from django.db import models


plan_choices=(
('P','Propagation'),
('PL','Planting'),
('V','Vegetative'),
('H','Harvest'),
('C','Cleaning'),
	)


class Plan(models.Model):
	field = models.ForeignKey('manager.Lot')
	crop = models.ForeignKey('manager.Crop')
	start_date = models.DateField(blank = False)

	def __unicode__(self):
		return str(self.field)+"-"+str(self.crop)
	
class PlanPart(models.Model):
	plan = models.ForeignKey('Plan')
	begin = models.DateField(blank = False, default=datetime.date.today)
	end = models.DateField(blank = False, default=datetime.date.today)
	plan_type = models.CharField(choices = plan_choices, max_length=2, blank = False)

	def __unicode__(self):
		return str(self.plan_type)

class PlanTemplate(models.Model):
	crop = models.ForeignKey('manager.Crop')
	days_propagation = models.IntegerField()
	days_planting = models.IntegerField()
	days_vegetative = models.IntegerField()
	days_harvest = models.IntegerField()
	days_cleaning = models.IntegerField()

	def __unicode__(self):
		return str(self.crop)
