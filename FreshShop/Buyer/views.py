from django.shortcuts import render
from django.shortcuts import HttpResponse

from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *

#===============密码校验=======================
import hashlib
def set_password(password):
    '''
    功能：用于对前端输入的密码进行加码
    '''
    md5 = hashlib.md5() # 重定义md5
    md5.update(password.encode())   # 密码加码
    pwd = md5.hexdigest()   # 转换为十六进制
    return pwd  # 返回
#===============用户校验=====================
def loginValid(fun):
    '''
    功能：用于校验各网页属于同一用户登录
    '''
    def inner(request,*args,**kwargs):
        # 获取cookies的值【存储在浏览器,存量有限】
        c_user = request.COOKIES.get('username')
        # 获取session的值【存储在服务器,存量无限】
        s_user = request.session.get('username')

        # 校验用户名成功(存cookies/session值且符等)
        if c_user and s_user and c_user == s_user:
            # 获取指定名称的【售卖方】
            user = Seller.objects.filter(username=c_user).first()
            if user:    # 售卖方存在
                return fun(request,*args,*kwargs)
        # 校验用户名成功,重新加载login
        return  HttpResponseRedirect('/buyer/login')
    return inner

# ================================================================================
# ================================================================================
# ===============【主页】=================================
def index(request):
    # goods_type_list = GoodsType.objects.all() # 存在bug[乱版/空类型]
    result_list = []#存储结果
    # username = request.user.username
    goodstype_list = GoodsType.objects.all() # 获取所有类型
    # 获取前四条数据并重新构建数据结构
    for goods_type in goodstype_list:
        goods_list = goods_type.goods_set.values()[:4] # 前四条
        if goods_list:  # 类型有对应值
            goodsType = {
                'id':goods_type.id,
                'name' :goods_type.name,
                'description':goods_type.description,
                'pirture':goods_type.picture,
                'goods_list':goods_list
            }
            result_list.append(goodsType)
    return render(request,'buyer/index.html',locals())
# ===============用户【注册页】=======================
from Buyer.forms import BuyerForm
def register(request):
    if request.method == 'POST':    # post请求
        # bf = BuyerForm(request.POST)    # 获取表单对象
        # if bf.is_valid():      # 表单数据准确
        username = request.POST.get('user_name')    # 前端【注册账号】
        password = request.POST.get('pwd')          # 前端【密码】
        email = request.POST.get('email')           # 前端【邮箱】
        # 保存数据
        buyer = Buyer() # 创建买方对象
        buyer.username = username                   # 保存账号
        buyer.password = set_password(password)     # 保存密码
        buyer.email = email                         # 保存邮箱
        buyer.save()
        # 注册成功后 重新加载login页
        return  HttpResponseRedirect('/login/')     # 返回登录页
    return render(request,'buyer/register.html')

# ===============用户【登录页】=======================
def login(request):
    if request.method == 'POST':
        # 获取【前端数据】
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 【校验用户】是否存在
        if username and password:
            # 获取用户
            user = Buyer.objects.filter(username=username).first()
            if user:
                # 对获取的前端密码加码
                web_password = set_password(password)
                # 校验密码
                if user.password == web_password:
                    response = HttpResponseRedirect('/index/')
                    # 校验登陆
                    request.session['username'] = user.username
                    response.set_cookie('username',username)
                    response.set_cookie('user_id',user.id)
                    return response
    return render(request,'buyer/login.html')
# ===============用户【退  出】=======================
def logout(request):
    response = HttpResponseRedirect('/login/')
    for key in request.COOKIES: # 获取当前请求的所有cookie
        response.delete_cookie(key)
    return response
# ===============用户【个人信息】=======================
def user_center_info(request):
    return render(request,'buyer/user_center_info.html')
# ===============用户【收货地址】=======================
def user_center_site(request):
    return render(request,'buyer/user_center_site.html')
# ===============用户【全部订单】=======================
def user_center_order(request):
    return render(request,'buyer/user_center_order.html')
# ===============【购物车】=======================
def cart(request):
    return render(request,'buyer/cart.html')
# ===============【查看更多】=======================
# 前端商品列表
def goods_list(request):
    goodsList = []
    type_id = request.GET.get('type_id')    # 获得类型id
    goods_type = GoodsType.objects.filter(id = type_id).first()
    if goods_type:
        # 获取所有上架商品
        goodsList = goods_type.goods_set.filter(goods_under=1)
    return render(request,'buyer/goods_list.html',locals())
# ===============【商品详情】=======================
def goods_detail(request):
    goods_id = request.GET.get('goods_id')
    if goods_id:
        goods = Goods.objects.filter(id = goods_id).first()
        if goods:
            return render(request, 'buyer/goods_detail.html', locals())
    return HttpResponseRedirect('没有您所指定的商品')




# 订单编号
import time
def setOrderId(user_id,goods_id,store_id):
    '''设置订单编号=时间+用户id+商品id+商铺+id'''
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime+user_id+goods_id+store_id


#===============用户【注册页】=======================
def base(request):
    return render(request,'buyer/base.html')


# def register(request):
#     if request.method == 'POST':
#         # 获取前端数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         # 保存数据
#         buyer = Buyer() # 创建买方
#         buyer.username = username
#         # 将前端密码加码后赋值给买方
#         buyer.password = set_password(password)
#         buyer.email = email
#         buyer.save()
#         # 注册成功后 重新加载login页
#         return  HttpResponseRedirect('/buyer/login')
#     return render(request,'buyer/register.html')











# 订单提交
def place_order(request):
    '''
    异常：django.db.utils.IntegrityError: NOT NULL constraint failed: Buyer_order.googd_count
    译文：IntegrityError: NOT NULL约束失败:Buyer_order.googd_count
    原因：
    解决方案：
    '''
    # if request.method == "POST":
    # 前端数据
    count = int(request.POST.get("count"))
    goods_id = request.POST.get("goods_id")
    user_id = request.COOKIES.get("user_id")#cookie的数据
    print(count,user_id,goods_id)
    # 数据库的数据
    goods = Goods.objects.get(id = goods_id)    # 根据商品id获取商品
    store_id = goods.store_id.get(id=5).id  #
    price = goods.goods_price
    print(goods,store_id,price)
    # 订单
    order = Order() # 创建一个订单对象
    order.order_id = setOrderId(str(user_id),str(goods_id),str(store_id))
    order.goods_count = count
    order.order_user = Buyer.objects.get(id = user_id)
    order.order_price = count*price
    print(order,order.order_id,order.goods_count,order.order_user,order.order_price)

    order.save()

    order_detail = OrderDetail()
    order_detail.order_id = order
    order_detail.goods_id = goods_id
    order_detail.goods_name = goods.goods_name
    order_detail.goods_price = goods.goods_price
    order_detail.goods_number = count
    order_detail.goods_total = count*goods.goods_price
    order_detail.goods_store = store_id
    order_detail.goods_image = goods.goods_image
    order_detail.save()

    detail = [order_detail]
    return render(request,"buyer/place_order.html",locals())
    # else:
    #     return HttpResponse("非法请求")




def pay_result(request):    # 支付结果
    """
    支付宝支付成功自动用get请求返回的参数
    #编码
    charset=utf-8
    #订单号
    out_trade_no=10002
    #订单类型
    method=alipay.trade.page.pay.return
    #订单金额
    total_amount=1000.00
    #校验值
    sign=enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    #订单号
    trade_no=2019072622001422161000050134
    #用户的应用id
    auth_app_id=2016093000628355
    #版本
    version=1.0
    #商家的应用id
    app_id=2016093000628355
    #加密方式
    sign_type=RSA2
    #商家id
    seller_id=2088102177891440
    #时间
    timestamp=2019-07-26
    """
    return render(request,"buyer/pay_result.html",locals())

def pay_order(request): # 订单支付
    money = request.GET.get("money") #获取订单金额
    order_id = request.GET.get("order_id") #获取订单id

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyXidUIBXbAxWYVERGPXImBc1yB+YsmBtymcwfZAu/UziPm+1spLu7Hq165erUpyFerY4KvY9GyqRJvkcTIEdn+0MJOX8wO4SbDiOtYzy+14dtYrora62jRYvbnkKDy6AWRoG5BML3rXRMUGtN4hAuy8s/lKqGtnO8NEouqMsd7xWaZyYyAzPpHhSrRMCkjojBJTt2iogCB+MzpJatBh0zDtdiGurPQNYAW1sFo8yK1C/FiYwCg8YWImwxoikpTBE3qGv5R7UHCOan0vbuLEJ0XFC8zE00vSi3nyh4LjBN7xf8Lqeeh9ntRUFj25vFSYMUHqXmR6qOYwS9rCV0ajr+wIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEAyXidUIBXbAxWYVERGPXImBc1yB+YsmBtymcwfZAu/UziPm+1spLu7Hq165erUpyFerY4KvY9GyqRJvkcTIEdn+0MJOX8wO4SbDiOtYzy+14dtYrora62jRYvbnkKDy6AWRoG5BML3rXRMUGtN4hAuy8s/lKqGtnO8NEouqMsd7xWaZyYyAzPpHhSrRMCkjojBJTt2iogCB+MzpJatBh0zDtdiGurPQNYAW1sFo8yK1C/FiYwCg8YWImwxoikpTBE3qGv5R7UHCOan0vbuLEJ0XFC8zE00vSi3nyh4LjBN7xf8Lqeeh9ntRUFj25vFSYMUHqXmR6qOYwS9rCV0ajr+wIDAQABAoIBAAfRTVFlWX8Qz31BNwef6eO06tpUF4m8YiY7cM8+fARKKnE/xm4ic3Drpgl5PiWbezZywaUxHtfiA/XeLrHtRKgC+7imz/Lwifh3DVqQGJGWalK0DClJIT5CQR7pRXGnXUWX0/KfppNCvNZLdRw1hkV9JCLONFmMYBJKG2l6kWwn6fluJbm7rxTy/y0r8sC2afsjPqZlRICF0iseGt9ENZ/8vtmnfrrkMMd0EhQMmZlJaN3coSoSSBsGnF5gLM+o2s09iy2Ppy6djbXZcyIn8IlEsiZ830Sn9erLyu9Wsay82Iu4z8XVijKN60hWVIFIwDFi9vzv0c/bMLn4NRbddjkCgYEA/miRkpDO0F9FPoubhD6k2R9UOEdr/Ze4M/N0gu3pkNKR3QtOvIlBq/Lw/Vdd2JI+VtbcoiciCqZbcRIhN9Q6Tmm0G/SAPd6qWhQKN+RwU6O2xOAJFHPixwzAONg2K/2ZHxhXNKg0O7wMDh0d+PU/cPZm0/PrQapdIACVUpslzc0CgYEAyrtEfYUeTiF0TJa7p1UtVDV2fNUXcBNafhwFLhw/G+1X4EjulhMywYjqAc+8G0uoL76vBoR0O8Vv2FHLeIKsoS5THDwJhc3b39yUl7Aa/e8woplYeM5JEWZAUCenbR4Zdb1ficR/jdAm4a0kyYRXnArvlicu51VmQhIZWAtFGOcCgYEAvx0uvjuqIT5wdhvKJ/4nODQgwGZm6YogBmbND85Jt1F34eWssFUr0FAgWTBYf2jdC78831Mmb3mpF7fW3GnBo0Yk1xtFezTaI/EJ/BLPjwVdN2hVadfkdENP42QIzeMkNAfE+vmgw37wT2nwKiWSEvoHJRIHmLyyWGgXxIZoT8ECgYEAsbDF7UaaM1z7NI4BWD8+Bcr+WZfkfSVZcaNZnvq/DdlP5pPGGuAk4qEAiinr8/iyJ3b4rbu2rRT2XSIEN1JBwNx7mAm/RvoSN/p8ex+t6NiXRk0l0GzuekOnJxo6k1eIdTxQ2s3SBxhkm/VIgyBuMaUcLf2WDMk7Ybm/YP4vyA0CgYBlxbrj5vRyb45F3fuVfOkwu3HuWU+HnGnnNNu7ZLv+oVTLX/VVjM0mvtVvQSpUcK3zQIrEmsed0QSZZ7UfPv7WAmjsHZ0q1V/bEF0UtGkVTg/XslUjvnUPRgwAqPP0V6o2fkf9EyJ4lfdt7KYE3TFahebwmf/CI9jka0yK0flcUw==
    -----END RSA PRIVATE KEY-----"""


    # 实例化支付应用
    from alipay import AliPay
    alipay = AliPay(
        appid="2016093000628354",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"
    )

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)