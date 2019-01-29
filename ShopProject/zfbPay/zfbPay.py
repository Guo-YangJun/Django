from alipay import AliPay

alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQAB
-----END PUBLIC KEY-----'''

app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpQIBAAKCAQEAwQ9irW5CqJKUpwADxuPeIGQJbvLwnrucVL/5Bg6dO903+tnuTsR7ziuxBqaaVFZefZAkimyXlFIUJ6mr3L/Zetx+YZWM80VioRcAFXhuKrFnFdr9oE6RCjoJjxqMRmbYSvmc2LOMLhTGKyZiznWPFHGQG3hpi5KSlSvjCUvbGRSTT9eyxMY9C7Z0A+8pB2vY7VYspUWcNaag4iLhFlga2De+IdmM8WcPh+2KagvPmS1Q2X3triSSSQpcDOlqq4zOwU0Pen7tGLeDoxKEmWyYvzzwo0lz+6mDRDLmt9weWc7uCVhY2o8s0C67Tph2V722jyc9avvmFXmz+9jXttvcCwIDAQABAoIBAQCwT2ezsS1pG6xsMwQ//9vcwt8mlvEOVZG4iDVYxcHsaOP10E7lWmUibR5XT5FDkjjq/NeSHwfzKV5EtpxAlmh73qAAaH53sJcZPJMUCI67qJXXDM5xNy8YItaV/Q28QbIoDnuiH57WepxbzcuQdyX66pdLrxTcpTf+yTynQcJOzLc+AKQQnF2DdXO/3/mDmkabMK4L1B0u9zQlIj4gvf3o5GJJaiQZvSEgjxerWRwE5f+wrNb37RNTEgNZ4i64qYYg3+0SVG+d+gxhzJvHJUZ68Bj3JBT5pIxV94lsExyDK89dfbMWJ6O1Fk5D3hrSJK5DFAsHmAtw8/2GCrmIGtA5AoGBAPDG4Hmhw04Jt3ITlS2KXBdW8fTsuMMkWoxIeWk3kHGJoHRYN5sMLMoKvgIoYS0sVGw/3K92eftRzFxXOw8NCFjKI7bYEUsZiLDNSR1pUOPmE3D0t3rF4ZxHbpAHpw/ewOMP5tksg1RZrN0oxEmdx0RsS2OEdm/Q8OA+mppjpJEdAoGBAM1ELuIdP4RAb6Yp+e8nlcnWG+i5y1A6a/IftM5kK8KMOs7m6KejTzE2MufzTaPvXl4VxqDIxwhY993cE3Y7sIsehnEPnMgVlIk03drHRqOhnEjUNcwjHwA1VaqY+IJQDuRKD7jD4yS6Z6jImFzI89J3TLp1rXaJhWHA7dhv+IFHAoGBAL885swU3H/eHdNAlIsQSubKyvDDGFj+ReEIK06TsGlNa6Ec9EV03Ro4gARMuCpd/EviSVEf4/DmXk+1hRYGPuvu2YD/inTAuh3bX0g5/uKUOjrMU/Lyuqga4EkLmvhy73cpiSxTO5hChZc/KvBhngTNku9fJYbYSImDj94yaGJNAoGAO5TSAwI4YJwPjGzcxmV4HhkPCtN7R3Ndx+8aHVqINTVdEJeH6rkFkKRJzHgcDjy56Jdri1ocI7knYXezEnuq+AbJQWIlwRI6hkUZLJrxTyfm5GDsqK99HSNeFWHHqJOybuNsgtYhRZTx59UqHKyb0XidhfYIfsLWO5SztUJzIJsCgYEA2QG2u/d+8dJQry76QU8SP8dELxUwHHAipVPALA7PMbgZBx2O5KWcXh9TdBjroT4NrO1O2HgyOTOLBaVMNgcziuK8WfHmZg9trFWLjGcsZYPYh056CNYZGcf5k1pk1BtRHJ0T0OefmCNErTqcHYrfovEUMg3hXo+nZXJfJv/wdI8=
-----END RSA PRIVATE KEY-----'''

# 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
# 在windows下，默认生成的txt文件，会有两个问题
# 1、格式不标准
# 2、编码不正确 windows 默认编码是gbk

# 实例化应用
alipay = AliPay(
    appid="2016092400585742",  # 支付宝app的id
    app_notify_url=None,  # 会掉视图
    app_private_key_string=app_private_key_string,  # 私钥字符
    alipay_public_key_string=alipay_public_key_string,  # 公钥字符
    sign_type="RSA2",  # 加密方法
)
# 发起支付
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="3345416",
    total_amount=str(999),  # 将Decimal类型转换为字符串交给支付宝
    subject="商贸商城",
    return_url=None,
    notify_url=None  # 可选, 不填则使用默认notify url
)

# 让用户进行支付的支付宝页面网址
print("https://openapi.alipaydev.com/gateway.do?" + order_string)