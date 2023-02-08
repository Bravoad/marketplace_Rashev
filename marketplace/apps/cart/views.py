from django.http import HttpRequest,HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView,UpdateView,FormView,View
from .cart import Cart
from ..catalog.forms import CartAddProductForm
from ..catalog.models import Product


# Create your views here.

class CartView(TemplateView):
    template_name = 'pages/cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = Cart(self.request)
        context['cart_total_price'] = Cart(self.request).get_total_price()

        return context


class CartAddView(View):

    def get(self,request,**kwargs):
        cart = Cart(self.request)
        pk = self.kwargs['product']
        prod = get_object_or_404(Product, id=int(pk))
        cart.add(product=prod,
                     quantity=int(self.request.GET.get('amount',default=1)),
                     update_quantity=0)
        return redirect('cart')

class CartRemoveView(View):

    def get(self,request,**kwargs):
        cart = Cart(self.request)
        pk = self.kwargs['product']
        print(pk)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product=product)
        return redirect('cart')
