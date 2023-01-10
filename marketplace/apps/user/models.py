from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField('Отчество',max_length=50,default='')
    balance = models.DecimalField('Баланс', default=0, decimal_places=2, max_digits=9)
    expired = models.DecimalField('Расходы', default=0, decimal_places=2, max_digits=9)
    avatar = models.ImageField(blank=True)

    @property
    def status(self):
        if self.expired <= 5000:
            return 'basic'
        elif 5000 <= self.expired <= 10000:
            return 'gold'
        elif self.expired >= 10000:
            return 'premium'

    def expired_add(self,price):
        self.expired += price

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
