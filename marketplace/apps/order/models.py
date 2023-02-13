from django.db import models
from apps.user.models import Profile
from apps.catalog.models import Product
from django.contrib.auth.models import User
# Create your models here.


class Delivery(models.Model):
    name = models.CharField('Наименование способа доставки',max_length=255)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField('Наименование способа оплаты',max_length=255)
    code = models.CharField('Код',max_length=255,default='')

    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,null=True,blank=True)
    delivery = models.ForeignKey(Delivery,on_delete=models.CASCADE)
    code = models.CharField('Номер банковской карты',max_length=20,default='',blank=True)
    city = models.CharField('Город',max_length=250,default='',blank=True)
    street = models.CharField('Улица',max_length=250,default='',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ №{}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
