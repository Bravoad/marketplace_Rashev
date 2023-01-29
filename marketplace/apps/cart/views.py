from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,UpdateView,FormView,View
from .cart import Cart
from ..catalog.forms import CartAddProductForm
from ..catalog.models import Product


# Create your views here.

class CartView(TemplateView):
    template_name = 'pages/cart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class CartAddView(FormView):

    def form_valid(self, form):
        cart = Cart(self.request)
        pk = self.kwargs['product']
        product = get_object_or_404(Product, id=pk)
        cart.add(product=product,
                     quantity=0,
                     update_quantity=1)
        return redirect('cart:cart_detail')


class CartRemoveView(FormView):

    def form_valid(self, form):
        cart = Cart(self.request)
        pk = self.kwargs['product']
        product = get_object_or_404(Product, id=pk)
        cart.remove(product=product)
        return redirect('cart:cart_detail')
