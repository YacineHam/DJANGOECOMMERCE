from django.shortcuts import render
from django.views.generic.list import ListView
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, guestOrder
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "store/store.html"
    context_object_name= 'products'
    
    def get_context_data(self,**kwargs):
        if self.request.user.is_authenticated:
            data= super().get_context_data(**kwargs)
            customer=self.request.user.customer
            order,created = Order.objects.get_or_create(customer=customer,completed=False)
            data['orderCount']=order.orders
            data['shipping']=order.shippingMethod
            return data
        else:
            data= super().get_context_data(**kwargs)
            cookieData= cookieCart(self.request)  
            data['orderCount']=cookieData['orderCount']
            data['shipping']=False
            return data
        
        
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,completed=False)
        orderTotal=order.orderTotal
        orderItems=order.orderitem_set.all()
        orderCount=order.orders
        shipping= order.shippingMethod
        context={'items':orderItems,'orderTotal':orderTotal,'orderCount':orderCount,'shipping':shipping}
    else:
        cookieData= cookieCart(request)  
        orderItems = cookieData['items']
        orderTotal = cookieData['orderTotal']
        orderCount = cookieData['orderCount']

        context={'items':orderItems,'orderTotal':orderTotal,'orderCount':orderCount,'shipping':False}

    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,completed=False)
        orderTotal=order.orderTotal
        orderItems=order.orderitem_set.all()
        orderCount=order.orders
        shipping= order.shippingMethod
    else:
        cookieData= cookieCart(request)  
        orderItems = cookieData['items']
        orderTotal = cookieData['orderTotal']
        orderCount = cookieData['orderCount']
        print(cookieData['shipping'])
        shipping= cookieData['shipping']
    return render(request,'store/checkout.html',{'items':orderItems,'orderTotal':orderTotal,'orderCount':orderCount,'shipping':shipping})


def updateItem(request):
    data=json.loads(request.body)
    productId= data['id']
    action   = data['action']
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,completed=False)
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderItem.quantity += 1
    elif action=='remove':
        orderItem.quantity -= 1
    orderItem.save()
    print(orderItem.quantity)
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('item was added',safe=False)

def proccesOrder(request):
    data = json.loads(request.body)
    tranasction_id=datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created= Order.objects.get_or_create(customer=customer,completed=False)
    else:
        customer,order = guestOrder(request,data)
        order.transaction_id=tranasction_id
        total = float(data['form']['total'])
        if total == order.orderTotal:
            order.completed=True
            order.save()
        if order.shippingMethod == True:
                    ShippingAdress.objects.create(
                    customer=customer,
                    order=order,
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    address=data['shipping']['address'],
                    zip_code=data['shipping']['zipcode']
                )
        
    return JsonResponse("Order Procesed",safe=False)

#def proccesOrder(request):
#    data = json.loads(request.body)
#    shippingInfo = data['shipping']
#    if request.user.is_authenticated:
#        customer = request.user.customer
#        order = Order.objects.get_or_create(customer=customer,completed=False)
#        order.transaction_id = datetime.now()
#        order.completed=True
#        address = ShippingAdress(customer=customer,order=order,city=shippingInfo['city'],state=shippingInfo['state'],address=shippingInfo['address'],zipcode=shippingInfo['zipcode'])
#    
#    return JsonResponse('order proceses',safe=False)