from django.shortcuts import render
from django.views.generic import TemplateView,UpdateView,FormView,View
from .cart import Cart
# Create your views here.

class CartView(TemplateView):
    template_name = 'pages/cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context
