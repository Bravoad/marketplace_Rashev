from django.db import models
from apps.user.models import Profile
from apps.catalog.models import Product
# Create your models here.


class Delivery(models.Model):
    name = models.CharField('Наименование способа доставки',max_length=255)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'


class Payment(models.Model):
    name = models.CharField('Наименование способа оплаты',max_length=255)
    code = models.CharField('Номер банковской карты',max_length=20,default='',blank=True)
    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery,on_delete=models.CASCADE)
    count = models.IntegerField('Количество товаров')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
