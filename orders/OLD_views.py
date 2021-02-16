from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import Customer, Order, Product, Note, DeletedRecurringOrder
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
import json

#Not to be confused with the get_recurring_orders webmethod below
def getrecurringorders(thedate):
    recurringorders = [o for o in Order.objects.filter(recurring=True).filter(recurring_days__icontains=str(thedate.weekday())).exclude(date__gte=thedate) 
                           if (
                                  (((thedate - o.date).days % (7 * o.recurring_frequency)) < 7)
                                  and
                                  not DeletedRecurringOrder.objects.filter(date=thedate, order=o).exists() 
                              )
                      ]
    return recurringorders

@login_required(login_url='/login/')
@permission_required('orders.add_order')
def main(request, year=-1, month=-1, day=-1):
    if(request.method=='POST'):
        requested_date = date(int(year),int(month),int(day))
    elif(int(year) > 0 and int(month) > 0 and int(day) > 0):
        requested_date = date(int(year),int(month),int(day))
    else:
        requested_date = date.today()
        if(datetime.now().hour < 10): 
            requested_date -= timedelta(days=1)
        requested_date += timedelta(days=1)#Visualizes tomorrow not today.
    allcustomers = Customer.objects.all()
    allproducts = Product.objects.all()
    orders = list(Order.objects.filter(date = requested_date).filter(deleted = False))
    customers = [c for c in allcustomers if any(o.customer.id == c.id for o in orders)]
    products = [p for p in  allproducts if any(p == o.product for o in orders)] 
    allproductsjson = '[' + ', '.join('"' + p.code  + '"' for p in allproducts) + ']'
    allcustomersjson = '[' + ', '.join('"' + c.name + '"' for c in allcustomers) + ']'
    productsjson = '[' + ', '.join('"' + p.code + '"' for p in products) + ']'    

    for c in customers:
        c.columns = [list() for p in products]
        c.checksum = 0
        n = Note.objects.filter(customer = c, date = requested_date).first()
        c.note = n.note if n else '' 
        c.PO = n.PO if n else ''
        if n and n.pallette:
            c.pallette = n.pallette       

    allpallettes = set(c.pallette for c in customers)

    for product in products:
        product.totals = dict()

    for o in orders:
        key = str(o)[len(str(o.quantity)):].split('|')[0]#example:4x30|5.55
        customers[customers.index(o.customer)].checksum += o.quantity
        customers[customers.index(o.customer)].columns[products.index(o.product)] += [o]
        product = products[products.index(o.product)]
        product.totals[key] = (product.totals[key] + o.quantity) if key in product.totals else o.quantity 
        o.new = (datetime.now() - o.created_time.replace(tzinfo=None)).total_seconds() < 900.0
        o.key = key

    totaloftotals = sum(c.checksum for c in customers)

    if request.method == 'POST':
        return render(request, 'orders/table.html', {'allpallettes':allpallettes, 'productsjson':productsjson, 'products':products, 'date':str(requested_date), 'customers':customers, 'totaloftotals':totaloftotals})
    else:
        return render(request, 'orders/main.html', {'allpallettes':allpallettes, 'productsjson':productsjson, 'allproductsjson':allproductsjson, 'allcustomersjson':allcustomersjson, 'products':products, 'date':str(requested_date), 'customers':customers, 'totaloftotals':totaloftotals})

@permission_required('orders.change_order')
def get_recurring(request):
	orders = Order.objects.filter(recurring=True).filter(deleted=False) 
	return render(request, 'orders/recurring_orders.html', {'orders': orders })

@permission_required('orders.change_order')
def history(request):
	orders = Order.objects.order_by('-created_time')[:100]
	return render(request, 'orders/history.html', {'orders': orders })

@permission_required('orders.change_note')
def change_note(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    customer=Customer.objects.get(id=int(request.POST['customer']))
    n, created = Note.objects.update_or_create(date=date, customer=customer, defaults={'note':request.POST['note']})
    return HttpResponse("success")

@permission_required('orders.change_note')
def change_po(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    customer=Customer.objects.get(id=int(request.POST['customer']))
    n, created = Note.objects.update_or_create(date=date, customer=customer, defaults={'PO':request.POST['PO']})
    return HttpResponse("success")

@permission_required('orders.change_note')
def change_pallette(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    customer=Customer.objects.get(id=int(request.POST['customer']))
    n, created = Note.objects.update_or_create(date=date,customer=customer, defaults={'pallette':request.POST['pallette'].lower()})
    return HttpResponse("success")

@permission_required('orders.change_order')
def change_order(request):
    o = Order.objects.get(id=int(request.POST.get("id")))
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    if(o.recurring):
        DeletedRecurringOrder.objects.create(order=o, date=date)
        o.pk = None    
        o.recurring = False
        o.date = date
    o.quantity = int(request.POST['quantity'])
    o.size = int(request.POST['size']) if request.POST['size'] else None
    o.special_unit_price = float(request.POST['special_unit_price']) if request.POST['special_unit_price'] else None
    o.save()
    return HttpResponse(request.POST.get('quantity'))
  
@permission_required('orders.delete_order')
def delete_order(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    o = Order.objects.get(id=int(request.POST.get("id")))
    if not o.recurring or request.POST.__contains__('deleterecurring'):
        o.delete()
    else:
        DeletedRecurringOrder.objects.create(order=o,date=date)
    return HttpResponse("Order Deleted!")
 
@permission_required('orders.delete_order')
def delete_recurring_order(request):
	order = Order.objects.get(id=int(request.POST.get("id")))
	order.deleted = True
	order.save()
	orders = Order.objects.filter(recurring=True).filter(deleted=False)

	return HttpResponse(orders)

@permission_required('orders.add_order')
@transaction.atomic
def add_order(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    customer = Customer.objects.get(name__iexact=request.POST['customer'])
    username = request.user.username
    recurring = bool(request.POST.get('recurring', False))
    frequency = int(request.POST['frequency'])
    days = ''.join(request.POST.getlist('recurring_days',''))

    orders = zip(*(request.POST.getlist(x) for x in ('quantity','product','price','size')))

    for quantity, product, price, size in orders:
        defaults = {
                    'quantity':quantity,
                    'recurring':recurring,
                    'created_user':request.user,
                    'recurring_frequency': frequency,
                    'recurring_days':days,
                   }
        params = {
                    'date':date,
                    'customer':customer,
                    'product':Product.objects.get(code__iexact=product),
                    'special_unit_price':price or None,
                    'size':size or None,
                 }

        order, new = Order.objects.get_or_create(defaults = defaults, **params)
        if not new:
            order.quantity += int(quantity)
            order.save()

    if not Note.objects.filter(date=date, customer=customer).exists():
        params = {
                     'date':date,
                     'customer':customer,
                     'note':request.POST.get('note',None),
                     'PO':request.POST.get('PO',None),
                     'pallette':request.POST['pallette'].lower() or None
                 }
        Note.objects.create(**params) 

    return HttpResponse('success')



