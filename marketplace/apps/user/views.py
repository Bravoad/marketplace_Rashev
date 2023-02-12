from django.views.generic import TemplateView,View,DetailView

from django.shortcuts import render,redirect
from django.db.models import Sum,F,Q
from django.contrib.auth.views import LoginView,LogoutView
from .forms import RegisterUserForm,BalanceForm,PeriodForm
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Profile
from apps.order.models import Order
from django.urls import reverse, reverse_lazy
import logging

# Create your views here.
logger = logging.getLogger(__name__)


class AuthView(LoginView):
    template_name = 'pages/login.html'

    def get_success_url(self):
        logger.info('Успешно перешёл на страницу')
        return reverse('main')


class LogView(LogoutView):
    template_name = 'pages/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info('Успешно перешёл на страницу')
        return context


class RegisterUser(TemplateView):
    template_name = 'pages/profile.html'


class RegisterCartUser(View):
    template_name = 'pages/step1.html'


class EditUser(TemplateView):
    template_name = 'pages/profile.html'


class UserDetailView(DetailView):
    model = User
    template_name = 'pages/account.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        logger.info('Успешно перешёл на страницу')
        context['order'] = Order.objects.select_related('delivery','delivery').filter(user=self.object).first()
        return self.render_to_response(context)


class CreateUser(View):

    def post(self,request):
        name = self.request.POST.get('name')
        mail = self.request.POST.get('mail')
        phone = self.request.POST.get('phone')
        password = self.request.POST.get('password')
        passwordreply = self.request.POST.get('passwordReply')
        user = User.objects.create(username=mail.split('@')[0],
                                   email=mail,
                                   password=password,
                                   password1=passwordreply)
        user.save()
        profile = Profile.objects.create(user=user,full_name=name,phone=phone)
        profile.save()
        return redirect('log-in')


class CreateCartUser(View):

    def post(self,request):
        name = self.request.POST.get('name')
        mail = self.request.POST.get('mail')
        phone = self.request.POST.get('phone')
        password = self.request.POST.get('password')
        passwordreply = self.request.POST.get('passwordReply')
        user = User.objects.create(username=mail.split('@')[0],
                                   email=mail,
                                   password=password,
                                   password1=passwordreply)
        user.save()
        profile = Profile.objects.create(user=user,full_name=name,phone=phone)
        profile.save()
        return redirect('log-in')
