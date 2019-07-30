from django.urls import path
from django.urls import re_path
from Buyer.views import *
urlpatterns = [
    path('', index),
    re_path('index/', index),

    path('register/', register),
    re_path('/login/',login),
    path('logout/',logout),

    path('goods_list/',goods_list),
    path('goods_detail/',goods_detail),
    path('place_order/',place_order),
    path('pay_result/',pay_result),
    path('pay_order/',pay_order),

]

urlpatterns += [
    path('base/',base),
]
