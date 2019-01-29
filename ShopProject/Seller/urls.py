from django.urls import path,re_path
from Seller.views import *
urlpatterns = [
    re_path('^$',index),
    path('index/',index),
    path('goods_add/',goods_add,name="goodsadd"),
    path('goods_list/',goods_list,name="goodslist"),
    re_path('goodslist/(\d+)/',goodslist),
    path('login/',login),
    path('example/',example),
    path('logout/',logout),
    re_path('goods/(\d+)/',goods),
    re_path('datadelete/(\d+)/',datadelete),
    re_path('change/(\d+)/',change),
    path('iform/',iform),
]
