from django.contrib import admin
from planner import models

PlannerModels=[models.Plan, models.PlanPart, models.PlanTemplate]

admin.site.register(PlannerModels)