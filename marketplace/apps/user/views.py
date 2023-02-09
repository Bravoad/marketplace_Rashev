from django.views import generic
from django.shortcuts import render
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


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'pages/step1.html'
    success_url = reverse_lazy('log-in')


class EditUser(generic.UpdateView):
    form_class = RegisterUserForm
    template_name = 'pages/profile.html'
    success_url = reverse_lazy('log-in')


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'pages/account.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        logger.info('Успешно перешёл на страницу')
        context['order'] = Order.objects.select_related('delivery','delivery').filter(user_id=self.get_object).last()
        return self.render_to_response(context)
