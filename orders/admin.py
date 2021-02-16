from django import forms
from django.contrib import admin
from .models import *



class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
        exclude = []

    code=forms.CharField(max_length=200, validators=[MinLengthValidator(3)])


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(DeletedRecurringOrder)
admin.site.register(Category)
admin.site.register(Note)