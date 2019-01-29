from django.shortcuts import render,HttpResponseRedirect
from Buy.models import *
from Seller.views import myencode
from Seller.models import Goods,Image,Seller
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
import random,datetime,time,os
from ShopProject.settings import MEDIA_ROOT
from alipay import AliPay

def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        username = cookie.get("name")
        session = request.session.get("user") #获取session
        user = Buy.objects.filter(username = username).first()
        if user and session == user.username: #校验session
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buy/login/")
    return inner

@cookieValid
def index(request):
    data=[]
    goods=Goods.objects.all()
    for i in goods:
        image=i.image_set.first()
        img=str(image.img_adress)
        data.append({'img':img,'name':i.goods_name,'price':i.goods_price,"id":i.id})
    return render(request,'buy/index.html',{'data':data})


def register(request):
    data=''
    if request.method=='POST' and request.POST:
        username=request.POST.get("username")
        password=request.POST.get("userpass")
        userpassword=request.POST.get("password")
        if userpassword==password:
            b=Buy()
            b.username=username
            b.password=myencode(password)
            b.save()
            return HttpResponseRedirect('/buy/login/')
        else:
            data="密码不一致！"
    return render(request, 'buy/register.html',{'data':data})

def registerPhone(request):
    data=''
    if request.method=='POST' and request.POST:
        username=request.POST.get("phone")
        password=request.POST.get("userpassword")
        userpassword=request.POST.get("password")
        if userpassword==password:
            b=Buy()
            b.username=username
            b.phone=username
            b.password=myencode(password)
            b.save()
            return HttpResponseRedirect('/buy/login/')
        else:
            data="密码不一致！"
    return render(request, 'buy/phone.html',{'data':data})

def login(request):
    data=''
    if request.method=='POST' and request.POST:
        name=request.POST.get('username')
        password=request.POST.get('userpass')
        user=Buy.objects.filter(username=name).first()
        email=Buy.objects.filter(email=name).first()
        phone=Buy.objects.filter(phone=name).first()
        if user or email or phone  and user.password==myencode(password):
            response=HttpResponseRedirect('/buy/index/')
            response.set_cookie('name',name)
            response.set_cookie('id',user.id)
            request.session['user']=name
            return response
        else:
            data='用户名或密码错误'
    return render(request, 'buy/login.html',{'data':data})

def logout(request):
    response = HttpResponseRedirect("/buy/login/")
    response.delete_cookie("name")
    response.delete_cookie("id")
    del request.session["user"]
    return response

def randomNum():
    num=random.randint(100000,999999)
    return num

def sendemail(request):
    data={"data":"返回值"}
    if request.method=="GET" and request.GET:
        email=request.GET.get("email")
        subject = "注册邮件"
        num=randomNum()
        text_content = "hello python"
        html_content ="""
            <p>尊敬的用户，你的验证码为%s</p>
        """%num
        message = EmailMultiAlternatives(subject,text_content,"18224516533@163.com",[email])
        message.attach_alternative(html_content,"text/html")
        message.send()
        check=CheckEmail()
        check.num=num
        check.time=datetime.datetime.now()
        check.email=email
        check.save()
    return JsonResponse(data)

def registerEmail(request):
    data=''
    if request.method=='POST' and request.POST:
        username=request.POST.get("email")
        password=request.POST.get("userpassword")
        userpassword=request.POST.get("password")
        code=request.POST.get("code")
        email = CheckEmail.objects.filter(email=username).first()
        if email and code==email.num:
            now=time.mktime(datetime.datetime.now().timetuple())
            old=time.mktime(email.time.timetuple())
            if now-old>=84600:
                data='验证码过期'
                email.delete()
            else:
                if userpassword==password:
                    b=Buy()
                    b.username=username
                    b.email=username
                    b.password=myencode(password)
                    b.save()
                    email.delete()
                    return HttpResponseRedirect('/buy/login/')
                else:
                    data="密码不一致！"
                    email.delete()
        else:
            data='验证码或邮箱错误'
            email.delete()
    return render(request, 'buy/email.html',{'data':data})

@cookieValid
def detail(request,num):
    all={}
    data=0
    allimg=[]
    good=Goods.objects.get(id=num)
    seller=good.seller.id
    goods=Goods.objects.filter(seller_id=seller)
    mg=good.image_set.all()
    for i in mg:
        allimg.append(str(i.img_adress))
    for i in goods:
        images=i.image_set.first()
        paths=(str(images.img_adress))
        if int(i.id)!=int(num) and data<=10:
            all[i]=paths
            data+=1
    img=good.image_set.first()
    path = str(img.img_adress)
    return render(request,'buy/details.html',locals())

@cookieValid
def car(request):
    id = request.COOKIES.get('id')
    add=Address.objects.filter(buyer=int(id))
    data=[]
    pay=0
    id=request.COOKIES.get("id")
    goodlist=BuyCar.objects.filter(user=int(id))
    for good in goodlist:
        money=float(good.price)*int(good.num)
        pay+=money
        data.append({'money':money,'good':good})
    return render(request,'buy/buyCar.html/',locals())

@cookieValid
def jump(request,goodid):
    id=request.COOKIES.get("id")
    good = Goods.objects.filter(id=int(goodid)).first()
    img = good.image_set.first()
    image = str(img.img_adress)
    if request.method=="POST" and request.POST:
        count=request.POST.get("count")
        money = float(good.goods_price) * int(count)
        butcar=BuyCar.objects.filter(user=int(id),goodId=goodid).first()
        if butcar:
            butcar.num+=int(count)
            butcar.save()
        else:
            car=BuyCar()
            car.goodId=goodid
            car.name=good.goods_name
            car.price=good.goods_price
            car.user=Buy.objects.get(id=int(id))
            car.num=int(count)
            car.picture=img.img_adress
            car.save()
    else:
        HttpResponseRedirect('/buy/login/')
    return render(request,'buy/jump.html/',locals())

@cookieValid
def delete(request,num):
    id = request.COOKIES.get("id")
    goods=BuyCar.objects.filter(user=int(id),goodId=num)
    goods.delete()
    return HttpResponseRedirect('/buy/car/')

@cookieValid
def clear(request):
    id = request.COOKIES.get("id")
    goods = BuyCar.objects.filter(user=int(id))
    goods.delete()
    return HttpResponseRedirect('/buy/car/')

@cookieValid
def address(request):
    id=request.COOKIES.get('id')
    if request.method=='POST' and request.POST:
        recver=request.POST.get('recver')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        add=Address()
        add.recver=recver
        add.phone=phone
        add.address=address
        add.buyer=Buy.objects.get(id=int(id))
        add.save()
        return HttpResponseRedirect('/buy/addressList/')
    return render(request,'buy/address.html')

@cookieValid
def addressList(request):
    id = request.COOKIES.get('id')
    add=Address.objects.filter(buyer=int(id))
    return render(request, 'buy/addressList.html', locals())

@cookieValid
def addressDel(request,id):
    add = Address.objects.filter(id=int(id))
    add.delete()
    return HttpResponseRedirect('/buy/addressList/')

@cookieValid
def addressChange(request,id):
    addChange=Address.objects.filter(id=int(id)).first()
    if request.method == 'POST' and request.POST:
        recver = request.POST.get('recver')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        addChange.recver = recver
        addChange.phone = phone
        addChange.address = address
        addChange.save()
        return HttpResponseRedirect('/buy/addressList/')
    return render(request, 'buy/address.html',locals())

@cookieValid
def orderAdd(request):
    buyId=request.COOKIES.get('id')
    list=[]
    all=[]
    if request.method=="POST" and request.POST:
        address=request.POST.get('address')
        pay=request.POST.get('pay')
        money=0
        for k,v in request.POST.items():
            if k.startswith('ok'):
                car=BuyCar.objects.get(id=int(v))
                price=float(car.num)*float(car.price)
                money+=price
                list.append({'price':price,'buy':car})
        Addr=Address.objects.get(id=int(address))
        order=Order()
        now=datetime.datetime.now()
        order.number=str(random.randint(10000,99999))+now.strftime("%Y%m%d%I%M%S")
        order.time=now
        order.statue=1
        order.money=money
        order.user=Buy.objects.get(id=int(buyId))
        order.orderAddress=Addr
        order.save()
        for i in list:
            good=i['buy']
            g=OrderGoods()
            g.goodsId=good.id
            g.goodsName=good.name
            g.goodsPrice=good.price
            g.goodsPicture=good.picture
            g.order=order
            g.goodsNum=good.num
            g.save()
        id=Order.objects.get(number=order.number)
        data=OrderGoods.objects.filter(order=id)
        for k in data:
            j=int(k.goodsNum)*float(k.goodsPrice)
            all.append({"money":j,"data":k})
        return render(request,'buy/order.html',locals())
    return HttpResponseRedirect('buy/car/')

@cookieValid
def openshop(request):
    if request.method=="POST" and request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        nickname=request.POST.get('nickname')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        email=request.POST.get('email')
        id_number=request.POST.get('id_number')
        photo=request.FILES.get('photo')
        s=Seller()
        s.username=username
        s.password=myencode(password)
        s.nickname=nickname
        s.phone=phone
        s.address=address
        s.email=email
        s.id_number=id_number
        s.photo = 'seller/img/' + photo.name
        path = os.path.join(MEDIA_ROOT, 'seller/img/%s' % photo.name)
        with open (path,'wb') as f:
            for j in photo.chunks():
                f.write(j)
        s.save()
        return HttpResponseRedirect('/seller/')
    return render(request,'buy/open.html')

@cookieValid
def allShop(request):
    shop=Seller.objects.all()
    return render(request,'buy/allShop.html',locals())

@cookieValid
def sellerShop(request,id):
    id=int(id)
    a=Seller.objects.get(id=id)
    data = []
    goods = a.goods_set.all()
    for i in goods:
        image = i.image_set.first()
        img = image.img_adress.url
        data.append({'img': img, 'name': i.goods_name, 'price': i.goods_price, "id": i.id})
    return render(request, 'buy/sellerShop.html', {'data': data,"a":a})

@cookieValid
def payMoney(request):
    data=""
    if request.method=="POST" and request.POST:
        money=request.POST.get("money")
        number=request.POST.get("number")
        alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
            MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQAB
        -----END PUBLIC KEY-----'''
        app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
            MIIEpQIBAAKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQABAoIBAQCwT2ezsS1pG6xsMwQ//9vcwt8mlvEOVZG4iDVYxcHsaOP10E7lWmUibR5XT5FDkjjq/NeSHwfzKV5EtpxAlmh73qAAaH53sJcZPJMUCI67qJXXDM5xNy8YItaV/Q28QbIoDnuiH57WepxbzcuQdyX66pdLrxTcpTf+yTynQcJOzLc+AKQQnF2DdXO/3/mDmkabMK4L1B0u9zQlIj4gvf3o5GJJaiQZvSEgjxerWRwE5f+wrNb37RNTEgNZ4i64qYYg3+0SVG+d+gxhzJvHJUZ68Bj3JBT5pIxV94lsExyDK89dfbMWJ6O1Fk5D3hrSJK5DFAsHmAtw8/2GCrmIGtA5AoGBAPDG4Hmhw04Jt3ITlS2KXBdW8fTsuMMkWoxIeWk3kHGJoHRYN5sMLMoKvgIoYS0sVGw/3K92eftRzFxXOw8NCFjKI7bYEUsZiLDNSR1pUOPmE3D0t3rF4ZxHbpAHpw/ewOMP5tksg1RZrN0oxEmdx0RsS2OEdm/Q8OA+mppjpJEdAoGBAM1ELuIdP4RAb6Yp+e8nlcnWG+i5y1A6a/IftM5kK8KMOs7m6KejTzE2MufzTaPvXl4VxqDIxwhY993cE3Y7sIsehnEPnMgVlIk03drHRqOhnEjUNcwjHwA1VaqY+IJQDuRKD7jD4yS6Z6jImFzI89J3TLp1rXaJhWHA7dhv+IFHAoGBAL885swU3H/eHdNAlIsQSubKyvDDGFj+ReEIK06TsGlNa6Ec9EV03Ro4gARMuCpd/EviSVEf4/DmXk+1hRYGPuvu2YD/inTAuh3bX0g5/uKUOjrMU/Lyuqga4EkLmvhy73cpiSxTO5hChZc/KvBhngTNku9fJYbYSImDj94yaGJNAoGAO5TSAwI4YJwPjGzcxmV4HhkPCtN7R3Ndx+8aHVqINTVdEJeH6rkFkKRJzHgcDjy56Jdri1ocI7knYXezEnuq+AbJQWIlwRI6hkUZLJrxTyfm5GDsqK99HSNeFWHHqJOybuNsgtYhRZTx59UqHKyb0XidhfYIfsLWO5SztUJzIJsCgYEA2QG2u/d+8dJQry76QU8SP8dELxUwHHAipVPALA7PMbgZBx2O5KWcXh9TdBjroT4NrO1O2HgyOTOLBaVMNgcziuK8WfHmZg9trFWLjGcsZYPYh056CNYZGcf5k1pk1BtRHJ0T0OefmCNErTqcHYrfovEUMg3hXo+nZXJfJv/wdI8=
        -----END RSA PRIVATE KEY-----'''
        alipay = AliPay(
            appid="2016092400585742",  # 支付宝app的id
            app_notify_url=None,  # 会掉视图
            app_private_key_string=app_private_key_string,  # 私钥字符
            alipay_public_key_string=alipay_public_key_string,  # 公钥字符
            sign_type="RSA2",  # 加密方法
        )
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=number,
            total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
            subject="商贸商城",
            return_url="http://127.0.0.1:8000/buy/car/",
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        data = ("https://openapi.alipaydev.com/gateway.do?" + order_string)
    return HttpResponseRedirect(data)

# Create your views here.
