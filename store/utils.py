from .models import *
import json
def cookieCart(request):
        try:
            
                cart = json.loads(request.COOKIES['cart'])
        except:
                cart = {}
                print(cart)
        items=[]
        context={'orderTotal':0,'orderCount':0,'shipping':True}
        total =0
        for i in cart:
            try:
                total +=cart[i]['quantity'] 
                product =Product.objects.get(id=i)
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
        return {'items':items,'orderTotal':context['orderTotal'],'orderCount':context['orderCount']}
   