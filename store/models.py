from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE,related_name='customer')
    name = models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name    = models.CharField(max_length=200)
    price   = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image   = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Order(models.Model):
    customer        = models.ForeignKey(Customer, verbose_name=("the related customer"), on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered    = models.DateTimeField(auto_now_add=True)
    completed       = models.BooleanField(default=False)
    transaction_id  = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def orderTotal(self):
        items=self.orderitem_set.all()
        total=sum([item.itemTotal for item in items])
        return total
    
    @property
    def orders(self):
        items=self.orderitem_set.all()
        total=sum([item.quantity for item in items])
        return total
    
    @property
    def shippingMethod(self):
        shipping=False
        for item in self.orderitem_set.all():
            if item.product.digital==False:
                shipping=True
        return shipping
    
    
    
class OrderItem(models.Model):
    product     = models.ForeignKey(Product, verbose_name=("related product"), on_delete=models.SET_NULL,null=True,blank=True)
    order       = models.ForeignKey(Order, verbose_name=("related order"), on_delete=models.SET_NULL,null=True,blank=True)
    quantity    = models.IntegerField(default=0,null=True,blank=True)
    date_added  = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    @property
    def itemTotal(self):
        return self.product.price * self.quantity
    
    
class ShippingAdress(models.Model):
    customer    = models.ForeignKey(Customer, verbose_name="related shipping adress", null=True,on_delete=models.SET_NULL)
    order       = models.ForeignKey(Order, verbose_name="related order", on_delete=models.SET_NULL,null=True)
    address     = models.CharField(max_length=200,null=True)
    city        = models.CharField(max_length=200,null=True)
    state       = models.CharField(max_length=200,null=True)
    zip_code    = models.CharField(max_length=200,null=True)
    date_added  = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.address