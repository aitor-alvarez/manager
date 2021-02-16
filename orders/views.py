from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from .models import Customer, Order, Product, Note, DeletedRecurringOrder
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from manager.models import Lot, Harvest
from utils.zpl_label import create_label
import json
from django.db.models import Q


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

def getrecurringordersproduct(thedate, products):
    recurringorders = [o for o in Order.objects.filter(recurring=True, product__in=products).filter(recurring_days__icontains=str(thedate.weekday())).exclude(date__gte=thedate) 
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
        if not request.POST.getlist('categories[]'):
            allproducts = Product.objects.all()
        else:
            categories = request.POST.getlist('categories[]')
            allproducts = Product.objects.filter(category__name__in=categories)
    elif(int(year) > 0 and int(month) > 0 and int(day) > 0):
        requested_date = date(int(year),int(month),int(day))
        allproducts = Product.objects.all()
    else:
        allproducts = Product.objects.all()
        requested_date = date.today()
        if(datetime.now().hour < 10): 
            requested_date -= timedelta(days=1)
        requested_date += timedelta(days=1)#They prefer to see tomorrow, not today.

    allcustomers = Customer.objects.all()
    if not request.POST.getlist('categories[]'):
        orders = list(Order.objects.filter(date = requested_date)) + getrecurringorders(thedate = requested_date)
        customers = [c for c in allcustomers if any(o.customer.id == c.id for o in orders)]
    else:
        orders  = list(Order.objects.filter(product__in=allproducts).filter(date = requested_date)) + getrecurringordersproduct(thedate = requested_date, products=allproducts)
        customers = [c for c in allcustomers if any(o.customer.id == c.id for o in orders)]
    products = [p for p in  allproducts if any(p == o.product for o in orders) ] 
    allproductsjson = '[' + ', '.join('"' + p.code  + '"' for p in allproducts) + ']'
    allcustomersjson = '[' + ', '.join('"' + c.name + '"' for c in allcustomers) + ']'
    productsjson = '[' + ', '.join('"' + p.code + '"' for p in products ) + ']'

    for c in customers:
        c.columns = [list() for p in products]
        c.checksum = 0   
        n = Note.objects.filter(customer = c, date = requested_date).first()
        
        c.note = n.note if n else '' 
        c.PO = n.PO if n else ''
        if n and n.pallette:
            c.pallette = n.pallette       

    allpallettes = set(c.pallette for c in customers)
    allcategories = set(p.category for p in products)
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
        return render(request, 'orders/table.html', {'allpallettes':allpallettes, 'allcategories': allcategories, 'productsjson':productsjson, 'products':products, 'date':str(requested_date), 'customers':customers, 'totaloftotals':totaloftotals})
    else:
        return render(request, 'orders/main.html', {'allpallettes':allpallettes, 'allcategories': allcategories, 'productsjson':productsjson, 'allproductsjson':allproductsjson, 'allcustomersjson':allcustomersjson, 'products':products, 'date':str(requested_date), 'customers':customers, 'totaloftotals':totaloftotals})

def login(request):
    return render(request, 'orders/login.html')

@permission_required('orders.change_order')
def get_recurring_orders(request):
    day = {'0':'Monday','1':'Tuesday','2':'Wednesday','3':'Thursday','4':'Friday','5':'Saturday','6':'Sunday'}
    orders = Order.objects.filter(recurring=True).order_by('customer__name')
    response = '<table id="recurringorderstable" class="table table-bordered"><thead><td></td><td>Customer</td><td>Order</td><td>Frequency</td><td>Days</td></thead>'

    deletebutton = '<div class="btn btn-xs text-success icon-btn btn-danger deleterecurringorderbutton" href="#"><span class="glyphicon btn-glyphicon glyphicon-remove img-circle text-danger"></span></div>'


    response += ''.join('<tr id="' + str(o.id) + '"><td>' + deletebutton 
                         + '</td><td>' + str(o.customer)
                         + '</td><td>' + str(o.product) + ' '  + str(o)
                         + '</td><td>Every ' + ('week' if (o.recurring_frequency == 1) else str(o.recurring_frequency) + ' weeks')
                         + '</td><td>' + ', '.join(day[c] for c in o.recurring_days) + '</td></tr>' 
                         for o in orders)
                         
   
    response += '</table>' 
    return render(request, 'orders/recurring_orders.html', {'context': response})

@permission_required('orders.change_order')
def get_history(request):
    orders = Order.objects.order_by('-created_time')[:100]
    response = '<table id="historytable" class="table table-bordered"><thead><td>Time Created</td><td>User</td><td>Customer</td><td>Order</td></thead>'
    response += ''.join('<tr id="' + str(o.id) + '"><td>' 
                        + o.created_time.strftime("%Y-%m-%d %H:%M:%S") 
                        + '</td><td>' + str(o.created_user) 
                        + '</td><td>' + str(o.customer)
                        + '</td><td>' + str(o.date) + ' ' + str(o.product) + ' ' +  str(o) + '</td></tr>'
                        for o in orders)
    response += '</table>'
    return HttpResponse(response)

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
    return HttpResponse(request.POST.get('quantity')) #What should I be putting here?
  
@permission_required('orders.delete_order')
def delete_order(request):
    date = datetime.strptime(request.POST['date'], "%m/%d/%Y").date()
    o = Order.objects.get(id=int(request.POST.get("id")))
    if Note.objects.filter(date=date, customer=o.customer).exists():
        Note.objects.filter(date=date, customer=o.customer).delete()

    if not o.recurring or request.POST.__contains__('deleterecurring'):
        if date.today()>=date:
            print "Cannot delete orders!"
        else:
            o.delete()
    else:
        DeletedRecurringOrder.objects.create(order=o,date=date)
    return HttpResponse("Order deleted!")

@permission_required('orders.delete_order')
def delete_recurring_order(request):
    today = datetime.now()
    date = today.strftime("%Y-%m-%d")
    o = Order.objects.get(id=int(request.POST.get("id")))
    if Note.objects.filter(date=date, customer=o.customer).exists():
        Note.objects.filter(date=date, customer=o.customer).delete()
    if(o.recurring):
        DeletedRecurringOrder.objects.create(order=o, date=date)   
        o.recurring = False
        o.date = date
        o.save()
    return HttpResponse("success!")
 
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
                    'size': size or None,
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


@permission_required('orders.change_order')
def history(request):
    if request.GET.get('customer'):
        customer = Customer.objects.filter(name__contains=request.GET.get('customer'))
        orders = Order.objects.filter(customer__in =customer).order_by('-created_time')[:300]
        return render(request, 'orders/history.html', {'orders': orders})

    else:
        orders = Order.objects.order_by('-created_time')[:100]
        return render(request, 'orders/history.html', {'orders': orders})


def trace_orders(request, date):
    orders = Order.objects.filter(date=date)
    thedate = datetime.strptime(date, "%Y-%m-%d").date()
    recurring_ids = [o.id for o in Order.objects.filter(recurring=True).filter(
        recurring_days__icontains=str(thedate.weekday())).exclude(date__gte=thedate)
                       if (
                               (((thedate - o.date).days % (7 * o.recurring_frequency)) < 7)
                               and
                               not DeletedRecurringOrder.objects.filter(date=thedate, order=o).exists()
                       )
                       ]
    recurringorders = get_recurring(recurring_ids, thedate)
    output = get_lots_order(orders, thedate)
    output = output + recurringorders
    if request.is_ajax():
        labels = {'labels':get_labels(output)}
        return HttpResponse(json.dumps(labels), content_type='application/json')
    else:
        return render(request, 'orders/trace_orders.html', {'orders': output, 'date': str(thedate)})


def get_lots_order(orders, thedate):
    data =[]
    for order in orders:
        crops = {'Garden': 3, 'Pea (Manoa Sugar)': 3, 'Winter Melon': 90, 'Tomatoes (Large Roma)': 3,
                 'Tomatoes (Assorted)': 3,
                 'Swiss Chard': 3, 'Squash Winter (Spaghetti)': 90, 'Squash Winter (Long)': 5, 'Squash Winter (Butternut)': 90, 'Okra': 5,
                 'Kale': 3,
                 'Eggplant (Round)': 5, 'Eggplant (Long)': 5, 'Cucumbers (Japanese)': 3, 'Beans (String)': 3,
                 'Beans (Long)': 3,
                 'Bitter Melon': 3}
        days = thedate - timedelta(days=crops[order.product.crop.name])
        harvest = Harvest.objects.filter(Q(crop=order.product.crop)& Q( created__gte=days)& Q(created__lte=thedate))
        lots = [str(h.lot.lot_name) for h in harvest]
        lots = list(set(lots))
        item = {"id": order.pk, "created": thedate, "customer": order.customer, "product": order.product, "quantity": order.quantity,
                 "size": order.size,"crop": order.product.crop.name, "lots": lots}
        data.append(item)
    return data


def get_recurring(ids, thedate):
    data=[]
    for id in ids:
        order= Order.objects.get(pk=id)
        crops ={'Garden': 3, 'Pea (Manoa Sugar)': 3, 'Winter Melon':90, 'Tomatoes (Large Roma)': 3, 'Tomatoes (Assorted)':3,
                'Swiss Chard': 3, 'Squash Winter (Spaghetti)': 90, 'Squash Winter (Long)': 5, 'Squash Winter (Butternut)': 90, 'Okra': 5,'Kale':3,
                'Eggplant (Round)': 5, 'Eggplant (Long)': 5, 'Cucumbers (Japanese)': 3, 'Beans (String)':3, 'Beans (Long)':3,
                'Bitter Melon':3}
        days = thedate - timedelta(days=crops[order.product.crop.name])
        harvest = Harvest.objects.filter(crop=order.product.crop, created__gte= days)
        lots = [str(h.lot.lot_name) for h in harvest]
        lots = list(set(lots))
        item = {"id": order.id, "created": thedate, "customer": order.customer, "product": order.product,
                "quantity": order.quantity, "size": order.size,
                "crop": order.product.crop.name, "lots": lots}
        data.append(item)
    return data


def get_labels(orders):
    labels = [create_label(order) for order in orders]
    labels = [l for sub in labels for l in sub]
    labels = ' '.join(labels)
    return labels


def get_labels_orders(request):
    orders=request.GET.getlist('orders[]')
    date = request.GET['date']
    print(orders)
    order_list = Order.objects.filter(id__in=orders).order_by('product__code')
    thedate = datetime.strptime(date, "%Y-%m-%d").date()
    output = get_lots_order(order_list, thedate)
    labels = {'labels': get_labels(output)}
    return HttpResponse(json.dumps(labels), content_type='application/json')