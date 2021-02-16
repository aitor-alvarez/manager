from django.contrib import admin
from manager import models

ManagerModels=[models.Lot, models.Crop, models.InputMethod, models.Brand, models.BrandUnit, models.Pest, models.Propagation, models.Method , 
models.Transplanting, models.Harvest, models.LotInfo, models.BrandGroup, models.Cleaning, models.CropUnit, models.HistorySettings, models.ItemShow]

admin.site.register(ManagerModels)


	