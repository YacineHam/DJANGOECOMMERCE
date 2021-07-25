from .models import *
import json
def cookieCart(request):
        try:
            
                cart = json.loads(request.COOKIES['cart'])
        except:
                cart = {}
                print(cart)
        items=[]
        context={'orderTotal':0,'orderCount':0,'shipping':False}
        total =0
        for i in cart:
            try:
                total +=cart[i]['quantity'] 
                product =Product.objects.get(id=i)
                
                if product.digital==False:
                    context['shipping']=True
                total = (product.price * cart[i]['quantity'])
                context['orderCount']+=cart[i]['quantity']
                context['orderTotal']+=total
                item = {
                    'product': {
                        'id': product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                    },
                    'quantity':cart[i]['quantity'],
                    'itemTotal':total
                }
                items.append(item)
            except:
                pass
        return {'items':items,'orderTotal':context['orderTotal'],'orderCount':context['orderCount'],'shipping':context['shipping']}
   
   
def guestOrder(request,data):
        print('user is not authenticated ')
        print(data)
        name = data['form']['name']
        email = data['form']['email']
        cookiecart = cookieCart(request)
        items = cookiecart['items']
        customer,created = Customer.objects.get_or_create(email=email)
        customer.name=name
        customer.save()
        order=Order.objects.create(
            customer=customer,
            completed=False,   
        )
        for item in items:
            product=Product.objects.get(id=item['product']['id'])
            orderItem=OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
        return customer,order
        
    
    
    
