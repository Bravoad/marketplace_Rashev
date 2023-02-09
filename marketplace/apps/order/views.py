from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView,UpdateView,DetailView,FormView,View
from .models import Order,OrderItem,Delivery,Payment
from apps.cart.cart import Cart
from .forms import OrderCreateForm
from apps.user.models import Profile
from apps.catalog.models import Product


class OrderListView(TemplateView):
    template_name = 'pages/historyorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.select_related('user','product','delivery','payment').filter(user=self.request.user.id)
        return context


class OrderView(TemplateView):
    template_name = 'pages/step2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery'] = Delivery.objects.all()
        return context


class OrderDetailView(DetailView):
    template_name = 'pages/oneorder.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.select_related('user','product','delivery','payment').filter(user=self.request.user.id)
        context['orders_items'] = OrderItem.objects.filter(items=self.get_object).all()
        return context


class OrderCartDetailView(DetailView):
    template_name = 'pages/step4.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carts'] = Cart(self.request)
        context['cart_total_price'] = Cart(self.request).get_total_price()
        return context

class OrderDeliveryView(TemplateView):
    template_name = 'pages/step2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery']=Delivery.objects.all()
        return context


class OrderPaymentDetailView(DetailView):
    template_name = 'pages/step3.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.all()
        return context


class OrderDeliveryCreateView(View):

    def post(self, request,**kwargs):
        city = self.request.POST.get('city')
        address = self.request.POST.get('address')
        delivery = self.request.POST.get('delivery')
        order = Order.objects.create(user=self.request.user,
                                     city=city,
                                     street=address,
                                     delivery=delivery)
        order.save()
        return reverse('payment',kwargs={'pk':order.id})


class PaymentCreateView(View):

    def post(self, request,**kwargs):
        cart = Cart(self.request)
        card = self.request.POST.get('numero1')
        order = self.kwargs['pk']
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity']
                                     )
            Product.objects.filter(id=item['product']).update(count=item['quantity'])
        Order.objects.filter(id=order).update(code=card,paid=True)
        cart.clear()
        return reverse('progress')


class OrderPaymentCreateView(View):

    def post(self, request, **kwargs):
        pay = self.request.POST.get('pay')
        order = self.kwargs['pk']
        Order.objects.filter(id=order).update(payment=pay)
        return reverse('order-payment',kwargs={'pk':order})


class PaymentSuccessView(TemplateView):
    template_name = 'pages/progressPayment.html'


class PaymentRandomView(TemplateView):
    template_name = 'pages/paymentsomeone.html'


class PaymentView(TemplateView):
    template_name = 'pages/payment.html'
