from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect   # 重定向
from Store.models import *

#============校验功能===================================
# 密码校验
import hashlib  # 导入hash模板
def set_password(password):
    '''对获取到的密码进行加密'''
    md5 = hashlib.md5() # 重新定义md5
    md5.update(password.encode())   # 指定加密方式
    pwd = md5.hexdigest()   # 转换为十六进制,并返回
    return pwd

# 登录校验
def loginValid(fun):
    '''
    bug:未对index进行登录校验,可以不用登录就可以进入到index页面；
    解决方案：使用装饰器对index页面进行校验
    '''
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            user = Seller.objects.filter(username=c_user).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect("/store/login/")
    return inner

def CookieTest(request):
    #查询拥有指定商品的所有店铺
    goods = Goods.objects.get(id = 1)
    store_list = goods.store_id.all()
    store_list = goods.store_id.filter()
    store_list = goods.store_id.get()
    #查询指定店铺拥有的所有商品
    store = Store.objects.get(id = 17)
    #goods是多对多表的名称的小写_set是固定写法
    store.goods_set.get()
    store.goods_set.filter()
    store.goods_set.all()

    response = render(request,"store/Test.html",locals())
    response.set_cookie("valid",'')
    return response
# ============视图===================================================

# 视图base(基本页)
def base(request):
    '''base页'''
    return render(request,'store/base.html')

@loginValid
# 视图index(首页)  【首页校验】
def index(request):
    '''检验账号是否具有店铺
        1、查询当前用户
        2、通过用户检查店铺是否存在(店铺与用户关联字段为用户id)
    '''
    # user_id = request.COOKIES.get("user_id")    # 获取用户id
    # if user_id: # 用户存在时
    #     user_id = int(user_id)
    # else:   # 用户不存在时
    #     user_id = 0
    # # 根据用户id获取店铺
    # store = Store.objects.filter(user_id=user_id).first()
    # if store:   # 店铺存在时
    #     is_store =  1   # True
    # else:
    #     is_store = 0    # False
    # # 给请求request返回一页面index.html,并将字典中的参数传递给页面index.html
    # # 在实现开发中,尽量少用locals()进行参数传递,原因：不安全,会显示在前端页面
    # return render(request,'store/index.html',{'is_store':is_store})
    user_id = request.COOKIES.get("user_id")
    user_name = request.COOKIES.get('username')
    if user_id: # 用户存在时
        user_id = int(user_id)
    else:   # 用户不存在时
        user_id = 0
    # 根据用户id获取店铺
    store = Store.objects.filter(user_id=user_id).first()
    if store:   # 店铺存在时
        is_store =  1   # True
    else:
        is_store = 0    # False
    # 给请求request返回一页面index.html,并将字典中的参数传递给页面index.html
    # 在实现开发中,尽量少用locals()进行参数传递,原因：不安全,会显示在前端页面
    return render(request,'store/index.html',{'is_store':is_store})

# 视图register(注册)
def register(request):
    '''注册页面'''
    result = {'content':''}
    if request.method == 'POST':
        # 获取请求request中包含的属性值
        request_username = request.POST.get('username')
        request_password1 = request.POST.get('password1')
        request_password2 = request.POST.get('password2')
        if request_username and request_password1 and request_password2:
            if request_password1 == request_password2:
                seller = Seller()   # 实例化一个卖方对象
                seller.username = request_username  # 姓名
                seller.nickname = request_username  # 昵称
                setpassword = set_password(request_password1)  # 加密
                seller.password = setpassword # 加密
                # seller.password = request_password1
                seller.save()
                result['content'] = '账号注册成功'
            else:
                result['content'] = '输入的密码不一致,请重新输入'
        else:
           result['content'] = '注册账号或密码不能为空'
    return render(request,'store/register.html',locals())

# 在登陆中使用密码校验功能
# @loginValid
def login(request):
    """
    登陆功能，如果登陆成功，跳转到首页
    如果失败，跳转到登陆页
    """
    response = render(request, 'store/login.html')
    response.set_cookie('login_from', 'login_page')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        if username and password:
            # 校验用户是否存在
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                # 校验请求是否来源于登陆页面
                cookies = request.COOKIES.get("login_from")
                # 校验密码是否正确
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/store/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id", user.id)  # cookie提供用户id方便其他功能查询
                    request.session["username"] = username
                    # 校验是否有店铺
                    store = Store.objects.filter(user_id = user.id).first()
                    if store:
                        response.set_cookie("has_store",store.id)
                    else:
                        response.set_cookie("has_store","")
                    return response
    return response

# 退出
def logout(request):
    response = HttpResponseRedirect('/store/login/')  # 重定向
    response.delete_cookie("username")
    return response

# 商铺注册
@loginValid
def register_store(request):
    '''店铺注册'''
    type_list=StoreType.objects.all()
    if request.method=='POST':
        post_data=request.POST
        store_name=post_data.get("store_name")
        store_descrition = post_data.get("store_descrition")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")

        user_id = int(request.COOKIES.get("user_id"))
        type_list = post_data.get("type")

        store_logo = request.FILES.get("store_logo")    # 获取图片或文件时,需使用FILES

        store = Store()
        store.store_name = store_name
        store.store_descrition = store_descrition
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo
        store.save()
        for i in type_list:
            store_type = StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
        # 商铺注册后,自动跳转到index页
        response = HttpResponseRedirect("/store/index")
        response.set_cookie("has_store",store.id)
        return response
    return render(request, "store/register_store.html", locals())
    # return render(request,'store/register_store.html')

# 商品添加
@loginValid
def goods_add(request):
    '''添加商品'''
    goodstype_list = GoodsType.objects.all()    # 获取所有商品类型(修改)
    if request.method == 'POST':
    # 获取poss请求中相关参数
        goods_name = request.POST.get('goods_name') # 商品名称
        goods_price = request.POST.get('goods_price') # 商品价格
        goods_number = request.POST.get('goods_number') # 商品库存数
        goods_description = request.POST.get('goods_description')   # 商品描述
        goods_date = request.POST.get('goods_date') # 出厂日期
        goods_safeDate = request.POST.get('goods_safeDate') # 保质期
        goods_store = request.POST.get('goods_store')   # 商铺
    # 图片或文件字段使用request.POST.get('goods_image') 无法上传图片或文件,需修改为FILES
        goods_image = request.FILES.get('goods_image')
        goods_type = request.POST.get('goods_type')
    # 获取的数据保存到数据库
        goods = Goods()   # 商品类对象
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_store = goods_store
        goods.goods_image = goods_image
        goods.goods_type = GoodsType.objects.get(id = int(goods_type))
        goods.save()    # 保存数据
    # 保存多对多数据
        # store_id 是goods模型中的关联字段
        goods.store_id.add(Store.objects.get(id=int(goods_store)))
        goods.save()
    return render(request,'store/goods_add.html',locals())

# 商品列表
from django.core.paginator import Paginator # 导入分页器类
@loginValid
def goods_list(request,state):
    # # 模糊查询
    # keywords = request.GET.get('keywords','')  # 获取搜索关键字,没关键字默认为空
    # page_num = request.GET.get('page',1)    # 获取页码,默认为页码为1
    # if keywords:
    #     # 有关键字，返回搜索结果
    #     goods_list = Goods.objects.filter(goods_name__contains=keywords)
    # else:
    #     goods_list = Goods.objects.all()
    # # 分页查询
    # paginator = Paginator(goods_list,3)     # 根据查询结果进行分页，每页3条记录
    # page = paginator.page(int(page_num))    # 获取页码
    # page_range = paginator.page_range
    # return render(request,'store/goods_list.html',{'page':page,'page_range':page_range,'keywords':keywords})
    # 获取两个关键字
    # 获取关键字和页码
    # 商品状态判断
    if state == 'up':
        state_num = 1
    else:
        state_num = 0
    keywords = request.GET.get("keywords", "")  # 关键词
    page_num = request.GET.get("page_num", 1)  # 页码
    # 通过cookies值获取店铺id
    # 来源店铺注册成功后所设置的cookies【response.set_cookie("has_store",store.id) 】
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))

    if keywords:  # 判断关键词是否存在
        # 完成了模糊查询(goods_under=state_num 商品状态)
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_under=state_num)
    else:  # 如果关键词不存在，按商品状态查询
        goods_list = store.goods_set.filter(goods_under=state_num)
    # 分页，每页3条
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    # 返回分页数据
    return render(request, "store/goods_list.html", {"page": page, "page_range": page_range, "keywords": keywords,'state':state})


# def goods(request,goods_id):
#     # 根据前端传入的商品id获取商品数据
#     goods_data = Goods.objects.filter(id = goods_id).first()
#     render(request,'store/goods.html',locals())

# 商品详情
@loginValid
def goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,"store/goods.html",locals())

# 商品修改
@loginValid
def goods_update(request,goods_id):
    # 根据goods_id查看商品信息
    goods_data = Goods.objects.filter(id = goods_id).first()
    if request.method == 'POST':
        # 获取post请求对象所包含的参数
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_number = request.POST.get('goods_number')
        goods_desctiption = request.POST.get('goods_description')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')
        goods_image = request.POST.get('goods_image')
        # 修改数据
        goods = Goods.objects.get(id = int(goods_id))   # 获取当前商品
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_desctiption
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect('/store/goods/%s'%goods_id)
    return render(request,"store/goods_update.html",locals())

# 商品状态
def set_goods(request,state):
    if state == 'up':
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get('id')# get方式获取商品id
    # 获取当前请求的来源地址(即当前页)
    referer = request.META.get('HTTP_REFERER')
    if id:
        # 获取指定id的商品
        goods = Goods.objects.filter(id = id).first()
        # 删除商品
        if state == 'delete':
            goods.delete()  # 删除
        else:
            goods.goods_under = state_num # 修改状态
            goods.save()
    # 重定向(重新访问指定页面)
    return HttpResponseRedirect(referer)

@loginValid
# 商品类型
def list_goodstype(request):
    goodstypelist = GoodsType.objects.all()
    if request.method == 'POST':
        # 获取数据
        name = request.POST.get('name')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')
        # 存储数据
        goodstype = GoodsType() # 创建对象
        goodstype.name = name
        goodstype.description = description
        goodstype.picture = picture
        goodstype.save()
        return HttpResponseRedirect('/store/list_goodstype')
    return render(request,'store/list_goodstype.html',locals())


