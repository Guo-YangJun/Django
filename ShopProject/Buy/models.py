from django.db import models

class Buy(models.Model):
    username = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    email = models.EmailField(blank = True,null = True)
    phone = models.CharField(max_length = 32,blank = True,null = True)
    photo = models.ImageField(upload_to = "buyer/images",blank = True,null = True)
    vip = models.CharField(max_length = 32,blank = True,null = True)

class Address(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length = 32)
    recver = models.CharField(max_length = 32)
    buyer = models.ForeignKey(Buy,on_delete = True)

class CheckEmail(models.Model):
    num=models.CharField(max_length=32)
    time=models.DateField(max_length=32)
    email=models.EmailField()

class BuyCar(models.Model):
    goodId = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    price = models.FloatField()
    picture = models.ImageField(upload_to="image")
    num = models.IntegerField()
    user = models.ForeignKey(Buy, on_delete=True)


class Order(models.Model):
    number = models.CharField(max_length = 32)  # 订单编号
    time = models.DateTimeField(auto_now = True)
    statue = models.CharField(max_length = 32)  # 订单状态
    money = models.FloatField()
    user = models.ForeignKey(Buy,on_delete = True)
    orderAddress=models.ForeignKey(Address,on_delete = True)

class OrderGoods(models.Model):
    goodsId=models.CharField(max_length = 32)
    goodsName=models.CharField(max_length = 32)
    goodsPrice=models.CharField(max_length = 32)
    goodsNum=models.CharField(max_length = 32)
    goodsPicture=models.CharField(max_length = 32)
    order=models.ForeignKey(Order,on_delete = True)