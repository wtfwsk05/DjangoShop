from django.urls import path,re_path
# 导入视图文件
from Store.views import *
urlpatterns = [
# 配置注册页面的路由
    path('register/', register),
    path('register_store/', register_store),
    path('list_goodstype/', list_goodstype),
    path('goods_add/', goods_add),
    re_path(r'goods_list/(?P<state>\w+)', goods_list),
    # path('goods_under/', goods_under),
    # re_path('goods/', goods),
    re_path(r'^goods/(?P<goods_id>\d+)', goods),
    re_path(r'goods_update/(?P<goods_id>\d+)', goods_update),
    re_path(r'set_goods/(?P<state>\w+)', set_goods),   # 商品状态
    path('login/', login),
    path('logout/', logout),
    path('index/', index),
]

urlpatterns += [
    path('base/',base),     # base页
    ]