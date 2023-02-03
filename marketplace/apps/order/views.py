from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView,UpdateView,DetailView,FormView,View
from .models import Order,OrderItem,Delivery,Payment
from apps.cart.cart import Cart
from  .forms import OrderCreateForm
from apps.user.models import Profile
from  apps.catalog.models import Product


class OrderListView(TemplateView):
    template_name = 'pages/historyorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.select_related('user','product','delivery','payment').filter(user=self.request.user.id)
        return context


class OrderDetailView(DetailView):
    template_name = 'pages/oneorder.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.select_related('user','product','delivery','payment').filter(user=self.request.user.id)
        context['orders_items'] = OrderItem.objects.filter(items=self.get_object).all()
        return context


class OrderCreateView(FormView):
    form_class = OrderCreateForm
    template_name = 'pages/order.html'

    def get_success_url(self):
        user=self.request.user.id
        return reverse('order-list')

    def form_valid(self, form):
        cart = Cart(self.request)
        product = Product.objects.get(pk=self.kwargs['pk'])
        user = Profile.objects.get(pk=self.request.user.id)
        form.instance.product = product
        form.instance.author = user
        form.instance.username = user.username
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()
        return super().form_valid(form)


class PaymentCreateView(FormView):
    form_class = OrderCreateForm
    template_name = 'pages/payment.html'

    def get_success_url(self):
        user=self.request.user.id
        return reverse('order-list',kwargs={'user':user})

    def form_valid(self, form):
        card = self.request.POST.get()
        return super().form_valid(form)
