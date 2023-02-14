from django.urls import path
from .views import OrderDetailView,OrderPaymentDetailView,OrderListView,PaymentRandomView,PaymentSuccessView,\
    PaymentCreateView,OrderDeliveryCreateView,OrderDeliveryView,OrderCartDetailView,OrderPaymentCreateView

urlpatterns = [
    path('order',OrderListView.as_view(),name='order-list'),
    path('order/delivery', OrderDeliveryView.as_view(), name='order-delivery'),
    path('order/<int:pk>',OrderDetailView.as_view(),name='order-detail'),
    path('order/create-delivery/',OrderDeliveryCreateView.as_view(),name='order-delivery-create'),
    path('order/<int:pk>/payment', OrderPaymentDetailView.as_view(), name='order-payment'),
    path('order/<int:pk>/cartdetail', OrderCartDetailView.as_view(), name='order-cart'),
    path('order/<int:pk>/payment/', PaymentCreateView.as_view(), name='payment-create'),
    path('order/<int:pk>/order-payment/', OrderPaymentCreateView.as_view(), name='order-payment-create'),

    path('order/<int:pk>/progress', PaymentSuccessView.as_view(), name='progress'),
    path('order/<int:pk>/random', PaymentRandomView.as_view(), name='random'),

]