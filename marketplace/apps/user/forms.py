from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    middle_name = forms.CharField(label='Отчество')
    username = forms.CharField(label='Логин')
    email = forms.EmailField()
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','middle_name', 'username', 'password1', 'password2')


class BalanceForm(forms.Form):
    balance=forms.IntegerField()


class PeriodForm(forms.Form):
    data_from=forms.DateTimeField()
    data_to=forms.DateTimeField()

