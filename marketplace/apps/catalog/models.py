from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    icon = models.FileField(blank=True,null=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True,unique=True)
    type = models.CharField(max_length=200,default='')
    image = models.ImageField(blank=True,null=True)
    is_popular = models.BooleanField('Популярный?',default=False,blank=True,null=True)
    is_banner = models.BooleanField('В баннер?',default=False,blank=True,null=True)
    is_limited = models.BooleanField('Ограниченный',default=False,blank=True,null=True)
    description = RichTextUploadingField('описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    comment = models.TextField('Комментарий')
    marks = models.IntegerField('Оценка', default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Attributes(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField('Наименование',max_length=250)
    value = models.CharField('Значение',max_length=250)

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'


class Sale(models.Model):
    title = models.CharField('Наименование',max_length=250)
    short_description = models.TextField('Краткое описание', default='')
    full_description = models.TextField('Полное Описание', default='')
    image = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'


class Gallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField('Наименование',max_length=250, default='')
    image = models.ImageField(blank=True,null=True)
