from django.views import generic
from django.shortcuts import render
from django.db.models import Sum,F,Q
from django.contrib.auth.views import LoginView,LogoutView
from .forms import RegisterUserForm,BalanceForm,PeriodForm
from django.contrib.auth.models import User
from django.core.cache import cache
from .models import Profile
from django.urls import reverse, reverse_lazy
import logging
class IndexView(generic.TemplateView):
    template_name = 'pages/account.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

"""
# Create your views here.
logger = logging.getLogger(__name__)

class AuthView(LoginView):
    template_name = 'news/login.html'
    def get_success_url(self):
        logger.info('Успешно перешёл на страницу')
        return reverse('main')


class LogView(LogoutView):
    template_name = 'news/logout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.info('Успешно перешёл на страницу')
        return context


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('log-in')

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'news/profile.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['order']=Order.objects.select_related('user_id','good_id').all()
        context['form']=BalanceForm()
        logger.info('Успешно перешёл на страницу')
        return self.render_to_response(context)
"""