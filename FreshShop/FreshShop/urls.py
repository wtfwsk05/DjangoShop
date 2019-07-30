"""FreshShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
'''
urls路由的匹配原则：
    1、为方便前端访问,并在访问时省略前端应用APP,其配置需在主urls.py文件中进行匹配；
    2、其他应用APP,为避免因重名所引起的冲突,可在各自的应用APP下的urls.py文件中进行匹配；
'''
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('Store.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

from Buyer.views import *
# from Buyer.views import index
# from Buyer.views import login
# from Buyer.views import logout
# from Buyer.views import register


urlpatterns = [
    re_path(r'^$', index),              # 什么都不匹配,默认执行index
    path('index/', index),              # 匹配index成功,执行index
    path('register/', register),        # 注册
    path('login/', login),              # 登录
    path('logout/', logout),            # 退出
    path('userinfo/', user_center_info),            # 个人信息
    path('userorder/', user_center_order),            # 我的订单
    path('cart/',cart),            # 购物车
    path('goodslist/',goods_list),            # 商品列表【查看更多】
    path('goodsdetail/',goods_detail),            # 商品详情
    path('placeorder/',place_order),            # 商品详情



    path('Buyer/', include('Buyer.urls')),
    ]
