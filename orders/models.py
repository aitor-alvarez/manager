from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.utils import timezone
from manager.models import Crop
from django.core.validators import MinLengthValidator

class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    pricing_type = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    pallette = models.CharField(max_length=20, default='pink')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Customer, self).save(*args, **kwargs)

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(3)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2) #A unit is 1 lb for loose or 1 package for packaged.
    size = models.IntegerField() #Either in pounds for loose or in number(e.g. 10 cucumbers) for packaged.
    packaged = models.BooleanField()
    description = models.CharField(max_length=200)    
    category = models.ForeignKey('Category', blank=True, verbose_name="Class")
    crop = models.ForeignKey(Crop, blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(Product, self).save(*args, **kwargs)

#Every order object and DB entry corresponds to a single product. 
#Therefore, ordering beans, tomatoes, and squash would be internally represented as 3 orders.
class Order(models.Model):
    class Meta:
        unique_together=(('date','customer','product','size','special_unit_price','recurring'),)

    date = models.DateField(default=timezone.now)
    created_time = models.DateTimeField(default=datetime.now)
    created_user = models.CharField(max_length=20)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product')
    finished = models.BooleanField(default=0)
    special_unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=None, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    size = models.IntegerField(default=None, null=True, blank=True)   
    recurring = models.BooleanField(default=False)
    recurring_frequency = models.IntegerField(default=1)
    recurring_days = models.CharField(max_length = 10, default=None, null=True, blank=True)#example: 014 is Monday, Tuesday, Friday. 67 is Saturday, Sunday 
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quantity) + ('x'+ str(self.size) if (self.size and (self.size != self.product.size)) else '') + (('|' + str(self.special_unit_price)) if (self.special_unit_price and (self.special_unit_price != self.product.unit_price)) else '')

class Note(models.Model):
    class Meta:
        unique_together=(('date','customer'),)
    date = models.DateField(auto_now=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    note = models.TextField(default=None, null=True)
    PO = models.CharField(max_length=200, default=None, null=True)
    pallette = models.CharField(max_length=20, default=None, null=True)


class DeletedRecurringOrder(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False)

    def __str__(self):
        return str(self.order)
class Category(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Class")

    def __str__(self):
        return str(self.name)
        
    class Meta:
        verbose_name ="Class"
        verbose_name_plural = "Classes"
