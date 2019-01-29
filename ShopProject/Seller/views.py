from Seller.models import *
import hashlib,os,datetime
from django.shortcuts import render
from  django.http import JsonResponse
from django.views.generic import View
from django.core.paginator import Paginator
from ShopProject.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect


def myencode(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

def cookieValid(cookiecheck):
    def inner(request,*args,**kwargs):
        cookie=request.COOKIES
        user=Seller.objects.filter(username=cookie.get("mycookie"))
        session=request.session.get("session")
        if user and user[0].nickname==session:
            return cookiecheck(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/seller/login/")
    return inner

def example(request):
    return render(request,"seller/test.html")

@cookieValid
def index(request):
    return render(request,"seller/index.html")

@cookieValid
def goods_add(request):
    t=Types.objects.all()
    if request.method=="POST" and request.POST:
        goods_id=request.POST.get("goods_num")       #浏览器form表单获取的数据
        goods_name=request.POST.get("goods_name")      #form表单内的name
        goods_price=request.POST.get("goods_oprice")
        goods_now_price=request.POST.get("goods_xprice")
        goods_num=request.POST.get("goods_count")
        goods_description=request.POST.get("goods_infro")
        goods_content = request.POST.get("goods_content")
        types=Types.objects.get(id=int(request.POST.get("type")))
        seller=Seller.objects.get(nickname=request.POST.get("username"))
        img=request.FILES.getlist("userfiles1")
        g = Goods()               #导入models.py中的Goods类
        g.goods_id=goods_id
        g.goods_name=goods_name
        g.goods_price=goods_price
        g.goods_now_price=goods_now_price
        g.goods_num=goods_num
        g.goods_show_time=datetime.datetime.now()
        g.goods_description = goods_description
        g.goods_content=goods_content
        g.types=types
        g.seller=seller
        g.save()   #数据保存关闭
        for k in img:
            i = Image()
            i.img_label = goods_name
            i.img_description = goods_description
            i.goods = Goods.objects.get(goods_id=goods_id)
            i.img_adress = 'seller/img/'+k.name
            path=os.path.join(MEDIA_ROOT,'seller/img/%s'%k.name)
            with open(path,"wb") as f:
                for j in k.chunks():
                    f.write(j)
            i.save()
    return render(request,"seller/goods_add.html",{"t":t})

@cookieValid
def goodslist(request,page):
    page = int(page)
    id = request.session.get("id")
    s = Seller.objects.get(id=id)
    db_student = s.goods_set.all()
    everone = Paginator(db_student, 1)  # 每一页的数据条
    count_data = everone.count  # 统计所有数据
    list = everone.page(page)  # 第一页数据
    # page_range=everone.page_range #页码范围
    pageEnd = count_data / 1
    if pageEnd != int(pageEnd):
        pageEnd = pageEnd + 1
    if page <=3:
        page_range = range(1, 6)
    elif page > pageEnd:
        page_range = range(1, 6)
    elif page >= pageEnd - 2:
        page_range = range(int(pageEnd)-4, int(pageEnd) + 1)
    elif page>3:
        page_range = range(page - 2, page + 3)
    return render(request,"seller/goods_list.html",locals())

@cookieValid
def goods_list(request):
    id=request.session.get("id")
    s=Seller.objects.get(id=id)
    db_student = s.goods_set.all() # 查询所有
    everone = Paginator(db_student, 1)  # 每一页10条
    list = everone.page(1)  # 第一页数据
    page_range = range(1, 6)
    return render(request,"seller/goods_list.html",locals())

@cookieValid
def goods(request,num):
    num=int(num)
    img=Image.objects.filter(goods_id=num)
    path=[]
    for i in img:
        path.append( i.img_adress.url)
    showgoods=Goods.objects.get(id=num)
    return render(request, "seller/goods.html", locals())

def login(request):
    data=""
    if request.method=="POST" and request.POST:
        name=request.POST.get("username")
        password=request.POST.get("password")
        check=request.POST.get("check")
        endcheck=request.COOKIES.get("endcheck")
        user=Seller.objects.filter(username=name)
        if user and user[0].password==myencode(password) and check=="check" and endcheck=="value_endcheck":
            response=HttpResponseRedirect("/seller/")
            response.set_cookie("mycookie",user[0].username)
            request.session["session"]=user[0].nickname
            request.session["id"]=user[0].id
            return response
        else:
            data="用户名或密码错误"
    response=render(request,"seller/login.html",{"data":data})
    response.set_cookie("endcheck","value_endcheck")
    return response

@cookieValid
def logout(request):
    mycookie=request.COOKIES.get("mycookie")
    if Seller.objects.filter(username=mycookie):
        response=HttpResponseRedirect('/seller/login/')
        response.delete_cookie("mycookie")
        response.delete_cookie("endcookie")
        del request.session["session"]
        return response
    else:
        return HttpResponseRedirect('/seller/login/')

@cookieValid
def datadelete(request,num):
    num=int(num)
    good = Goods.objects.get(id=num)     # 删除指定id的一条数据
    img=good.image_set.all()            #删除物品表图片对应的图片外键库中的图片表数据
    for i in img:                      #图片保存在数据库中的是地址，查到本地文件内对应的图片用os.remove删除本地图片
        path = os.path.join(MEDIA_ROOT,'%s'%str(i.img_adress))
        print(i.img_adress.url)
        os.remove(path)
    img.delete()
    good.delete()
    return HttpResponseRedirect('/seller/goods_list')

def iform(request):
    return render(request,'seller/iframeExample.html')

@cookieValid
def change(request,num):
    good=Goods.objects.get(id=int(num))     #修改对应id的数据
    if request.method=="POST" and request.POST:
        goods_id=request.POST.get("goods_num")
        goods_name=request.POST.get("goods_name")
        goods_price=request.POST.get("goods_oprice")
        goods_now_price=request.POST.get("goods_xprice")
        goods_num=request.POST.get("goods_count")
        goods_description=request.POST.get("goods_infro")
        goods_content = request.POST.get("goods_content")
        types=Types.objects.get(id=int(request.POST.get("type")))
        seller=Seller.objects.get(nickname=request.POST.get("username"))
        img=request.FILES.getlist("userfiles1")
        g = Goods.objects.get(id=int(num))
        images = g.image_set.all()
        images.delete()
        g.goods_id=goods_id
        g.goods_name=goods_name
        g.goods_price=goods_price
        g.goods_now_price=goods_now_price
        g.goods_num=goods_num
        g.goods_show_time=datetime.datetime.now()
        g.goods_description = goods_description
        g.goods_content=goods_content
        g.types=types
        g.seller=seller
        g.save()
        for k in img:
            i = Image()
            i.img_label = goods_name
            i.img_description = goods_description
            i.goods = Goods.objects.get(goods_id=goods_id)
            i.img_adress = 'seller\\img\\'+k.name
            path=os.path.join(MEDIA_ROOT,'seller\\img\\%s'%k.name)
            with open(path,"wb") as f:
                for j in k.chunks():
                    f.write(j)
            i.save()
        return HttpResponseRedirect('/seller/goods_list')
    return render(request,'seller/change.html',{"good":good})

class WeiXinApi(View):
    def __init__(self,**kwargs):
        View.__init__(self,**kwargs)
        self.response={
            "statue":"error",
            "data":""
        }
    def get(self,request):
        if request.GET:
            data = request.GET
            types = data.get('Type')
            order = data.get('order')
            all = data.get('all')
            if order and all == 'ture':
                self.response['data']="参数冲突"
            if all == 'ture':
                goodsList = []
                goods = Goods.objects.all()
                for i in goods:
                    goodsList.append({
                        'name':i.goods_name,
                        'num':i.goods_num,
                        'price':i.goods_now_price
                                      })
                self.response["statue"] = "success"
                self.response["data"] = goodsList
            if order:
                goods=Types.objects.get(label = order).goods_set.all()
                goodsList=[]
                for i in goods:
                    goodsList.append({
                        'name': i.goods_name,
                        'num': i.goods_num,
                        'price': i.goods_now_price
                    })
                self.response["statue"] = "success"
                self.response["data"] = goodsList
        return JsonResponse(self.response)

# Create your views here.
