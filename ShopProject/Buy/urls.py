from django.urls import path,re_path
from Buy.views import *

urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('login/', login),
    path('register/', register),
    path('registerEmail/', registerEmail),
    path('registerPhone/', registerPhone),
    path('logout/', logout),
    path('sendemail/', sendemail),
    re_path('detail/(\d+)/', detail),
    re_path('jump/(\d+)/', jump),
    re_path('delete/(\d+)/', delete),
    path('car/', car),
    path('clear/', clear),
    path('address/', address),
    path('addressList/', addressList),
    path('openshop/', openshop),
    path('allShop/', allShop),
    path('payMoney/', payMoney),
    re_path('addressDel/(\d+)/', addressDel),
    re_path('addressChange/(\d+)/', addressChange),
    re_path('orderAdd/', orderAdd),
    re_path('sellerShop/(\d+)/', sellerShop),

]
