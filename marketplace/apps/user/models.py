from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField('ФИО',max_length=256, default='')
    phone = models.CharField('Номер телефона',max_length=20,default='')
    avatar = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
