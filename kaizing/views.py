from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.template import loader
from forms import *
from django.contrib import messages
from collections import Counter
import re

# Create your views here.
def index(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    orders = Order.objects.filter(vendor=vendor)
    hack = 0
    if 'login' in request.session:
        ven_id = request.session['login']
        if ven_id != '2xgvrfTV'+str(vendor_id)+'xF232nh':
            hack = 1
    else:
        hack = 1
    if hack == 1:
        return render(request,'kaizing/hackers.html')
    context = {'orders': orders, 'vendor': vendor}
    return render(request, 'kaizing/order_display.html', context)


def viewitem(request, item_id):
    obje = get_object_or_404(Item, pk=item_id)

    context = {'object': obje}

    return render(request, 'kaizing/number.html', context)


def cancelorder(request, order_id, vendor_id):
    context = {}
    order_to_cancel = get_object_or_404(Order, pk=order_id)
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context['vendor'] = vendor
    orders = Order.objects.all()
    context['orders'] = orders
    order_to_cancel.order_state = Order.ORDER_STATE_CANCELLED
    # order_to_cancel.modified = datetime.date.today()
    order_to_cancel.save()
    # return render(request, 'kaizing/order_display.html', context)
    return redirect("kaizing:index", vendor_id)


def vieworder(request, order_id, vendor_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {}
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context['vendor'] = vendor
    orders = Order.objects.all()
    context['orders'] = orders
    context['order'] = order
    
    orderitems=order.items.split(':')[1].replace('}','').split(',')
    items = Item.objects.all()
    itemslist = []
    for orderitem in orderitems:
        for item in items:
            if item.pk == int(orderitem):
                itemslist.append(item.name)
    itemsnamelist = Counter(itemslist)
    
    itemscountlist=[]
    for x in itemsnamelist:
        itemscountlist.append(itemsnamelist[x])
    
    itemslist = {}
    
    for x,y in zip(itemsnamelist,itemscountlist):
        itemslist[x]=y
    
    context['itemslist'] = itemslist
    
    return render(request, 'kaizing/vieworder.html', context)


def vendorlogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username and not password:
        form = VendorLoginForm()
    elif username:
        form = VendorLoginForm(request.POST)
    else:
        form = VendorLoginForm()
    context = {}
    context['form'] = form
    if request.method == 'POST':
        try:
            vendor_to_match = get_object_or_404(Vendor, username=username)
        except:
            vendor_to_match = False
        if not vendor_to_match:
            messages.error(request, "Invalid Username")
            return render(request, 'kaizing/vendorlogin.html', context)
        if vendor_to_match.password == password:
            vendor_to_match.is_authenticated = True
            vendor_to_match.save()
            request.session['login']='2xgvrfTV'+str(vendor_to_match.pk)+'xF232nh'
            return redirect('kaizing:index',vendor_to_match.id)
        else:
            messages.error(request, "Invaid Password")
    return render(request, 'kaizing/vendorlogin.html', context)


def vendorlogout(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    vendor.is_authenticated = False
    vendor.save()
    return redirect('kaizing:vendorlogin')


def acknowledgeorder(request, order_id, vendor_id):
    context = {}
    order_to_cancel = get_object_or_404(Order, pk=order_id)
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context['vendor'] = vendor
    orders = Order.objects.all()
    context['orders'] = orders
    order_to_cancel.order_state = Order.ORDER_STATE_ACKNOWLEDGED
    # order_to_cancel.modified = datetime.date.today()
    order_to_cancel.save()
    # return render(request, 'kaizing/order_display.html', context)
    return redirect('kaizing:vieworder', vendor_id, order_id)


def completeorder(request, order_id, vendor_id):
    context = {}
    order_to_cancel = get_object_or_404(Order, pk=order_id)
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context['vendor'] = vendor
    orders = Order.objects.all()
    context['orders'] = orders
    order_to_cancel.order_state = Order.ORDER_STATE_COMPLETED
    # order_to_cancel.modified = datetime.date.today()
    order_to_cancel.save()
    # return render(request, 'kaizing/order_display.html', context)
    return redirect('kaizing:vieworder', vendor_id, order_id)


def dispatchorder(request, order_id, vendor_id):
    context = {}
    order_to_cancel = get_object_or_404(Order, pk=order_id)
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    context['vendor'] = vendor
    orders = Order.objects.all()
    context['orders'] = orders
    order_to_cancel.order_state = Order.ORDER_STATE_DISPATCHED
    # order_to_cancel.modified = datetime.date.today()
    order_to_cancel.save()
    # return render(request, 'kaizing/order_display.html', context)
    return redirect('kaizing:vieworder', vendor_id, order_id)


#############################################################################################################
# Frontend Views

def home(request):
    return render(request, 'kaizing/index.html')


def menudisplay(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    genres = vendor.genre.all()
    # arr = [[item.pk] for item in genres.item.all()]
    arr1 = []
    for genre in genres:
        arr2 = []
        for item in genre.item.all():
            arr2.append(item.pk)
        arr1.append(arr2)
        
    items = Item.objects.all()
    totalnoitems = len(items)
    context = {}
    context['vendor_id'] = vendor_id
    context['totalnoitems'] = totalnoitems
    context['itemgenrelist'] = arr1
    context['genres'] = genres
    context['items'] = items
    context['vendescription'] = vendor.description
    context['venlocation'] = vendor.location
    context['venname'] = vendor.name
    context['isopen'] = vendor.is_open
    context['deliverytime'] = vendor.delivery_time
    return render(request, 'kaizing/menu.html', context)


def checkout(request):
    if request.POST:
        newOrder = Order()
        newOrder.phone=request.POST['phone']
        newOrder.email=request.POST['email']
        newOrder.name=request.POST['name']
        slots = timeSlot.objects.all()
        orderLocation=0
        ordertimeSlot=0
        orderVendor=0
        for slot in slots:
            if slot.pk == int(request.POST['timeslot']):
                ordertimeSlot = slot
                break
        newOrder.slot=ordertimeSlot
        locations = location.objects.all()
        for locate in locations:
            if locate.id == int(request.POST['location']):
                orderLocation = locate
                break
        newOrder.delivery_address=orderLocation
        vendors = Vendor.objects.all()
        for vendor in vendors:
            if vendor.pk == int(request.POST['vendor']):
                orderVendor = vendor
                break
        newOrder.vendor=orderVendor
        itemids = request.POST['cart'].split(',')
        for item in itemids:
            queryset = Item.objects.get(pk=int(item))
            queryset.num=int(queryset.num)-1
            queryset.save()
            if int(queryset.num) == 0:
                queryset.isavailable = False
                queryset.save()
            
        newOrder.items='{"id":'+request.POST['cart']+'}'
        newOrder.order_total=float(request.POST['total'])
        newOrder.save()
        orderid = 'KZ'+newOrder.vendor.alias.upper()+str(newOrder.delivery_address.name)+str(newOrder.pk)
        context={
            "id": orderid,
        }
        return render(request,'kaizing/orderconfirm.html',context)
    else:
        items = list(Item.objects.all())
        locations = location.objects.all()
        allSlots = timeSlot.objects.all()
        availSlots = []
        for x in allSlots:
            if x.max_limit > datetime.datetime.now().time():
                availSlots.append(x)
        vendors = Vendor.objects.all()
        allvendors=[]
        for vendor in vendors:
            allvendors.append(vendor)
        context = {
            "items": items,
            "locations":locations,
            "slots":availSlots,
            "allvendors": allvendors,
        }
        return render(request, 'kaizing/checkout.html',context)


def vendordisplay(request):
    vendors = Vendor.objects.all()
    genres = Genre.objects.all()
    items = Item.objects.all()
    # items = genres[1].item.all()
    context = {}
    context['vendors'] = vendors
    context['genres'] = genres
    context['items'] = items

    return render(request, 'kaizing/vendor_display.html', context)

def orderstatus(request):
    if request.POST:
        orderid = request.POST['id']
        orderid=re.findall('\d+',orderid)
        if len(orderid) < 1:
            context = {
                'error' : '1',
                'mode' : '0',
            }
            return render(request,'kaizing/orderquery.html',context)
        thisorder = Order.objects.all().filter(pk=int(orderid[0]))
        if len(thisorder) == 0:
            context = {
                'error' : '1',
                'mode' : '0',
            }
            return render(request,'kaizing/orderquery.html',context)
        thisorder = thisorder[0]
        orderitems=thisorder.items.split(':')[1].replace('}','').split(',')
        items = Item.objects.all()
        itemslist = []
        for orderitem in orderitems:
            for item in items:
                if item.pk == int(orderitem):
                    itemslist.append(item.name)
        itemsnamelist = Counter(itemslist)
        itemscountlist=[]
        for x in itemsnamelist:
            itemscountlist.append(itemsnamelist[x])
        itemslist = {}
        for x,y in zip(itemsnamelist,itemscountlist):
            itemslist[x]=y
        context = {
            'id' : request.POST['id'],
            'name' : thisorder.name,
            'phone' : thisorder.phone,
            'email' : thisorder.email,
            'slot' : thisorder.slot,
            'address': thisorder.delivery_address,
            'total' : thisorder.order_total,
            'status' : thisorder.order_state,
        }
        context['itemslist'] = itemslist
        context['mode'] = '1'
        return render(request,'kaizing/orderquery.html',context)
    else:
        context = {
            'mode' : '0',
        }
        return render(request,'kaizing/orderquery.html',context)