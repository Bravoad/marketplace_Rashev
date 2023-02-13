from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView,UpdateView,DetailView,FormView,View
from .models import Order,OrderItem,Delivery,Payment
from apps.cart.cart import Cart
from apps.user.models import Profile
from apps.catalog.models import Product
from django.db.models import F


class OrderListView(TemplateView):
    template_name = 'pages/historyorder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.select_related('user','delivery','payment').filter(user=self.request.user.id)
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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['orders_items'] = OrderItem.objects.filter(order=self.object).all()
        return self.render_to_response(context)


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


class OrderDeliveryCreateView(View):

    def post(self, request,**kwargs):
        city = self.request.POST.get('city')
        address = self.request.POST.get('address')
        delivery = Delivery.objects.get(id=self.request.POST.get('delivery'))
        order = Order.objects.create(user_id=self.request.user.id,
                                     city=city,
                                     street=address,
                                     delivery=delivery)
        order.save()
        print(order)
        return redirect('order-payment',order.id)


class OrderPaymentDetailView(DetailView):
    template_name = 'pages/step3.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = Payment.objects.all()
        return context


class OrderPaymentCreateView(View):

    def post(self, request, **kwargs):
        pay = self.request.POST.get('pay')
        order = self.kwargs['pk']
        Order.objects.filter(id=order).update(payment=pay)
        return redirect('order-cart',order)


class PaymentSuccessView(TemplateView):
    template_name = 'pages/progressPayment.html'


class PaymentRandomView(TemplateView):
    template_name = 'pages/paymentsomeone.html'


class PaymentView(TemplateView):
    template_name = 'pages/payment.html'


class PaymentCreateView(View):

    def post(self, request,**kwargs):
        cart = Cart(self.request)
        card = self.request.POST.get('numero1')
        order = Order.objects.get(id=self.kwargs['pk'])

        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity']
                                     )

            Product.objects.filter(id=item['product'].id).update(count=F('count')-item['quantity'])
        if int(card.replace(' ',''))%2 == 0 and int(card[-1]) != 0:
            Order.objects.filter(id=order.id).update(code=card,paid=True)
        else:
            Order.objects.filter(id=order.id).update(code=card)

        cart.clear()
        return redirect('order-detail', order.id)


