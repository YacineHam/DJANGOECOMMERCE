from django.urls import path
from .views import *


urlpatterns = [
    path('',ProductListView.as_view(),name='store'),
    path('checkout/',checkout,name='checkout'),
    path('cart/',cart,name='cart'),
    path('update_cart/',updateItem,name='update'),
    path('process_order/',proccesOrder,name='process')

]
