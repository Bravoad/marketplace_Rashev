from django.urls import path
from .views import OrderDetailView,OrderPaymentDetailView,OrderListView,PaymentRandomView,PaymentSuccessView,\
    PaymentCreateView,OrderDeliveryCreateView,OrderDeliveryView,OrderCartDetailView

urlpatterns = [
    path('order',OrderListView.as_view(),name='order-list'),
    path('order/delivery', OrderDeliveryView.as_view(), name='order-delivery'),
    path('order/<int:pk>',OrderDetailView.as_view(),name='order-detail'),
    path('order/<int:pk>/delivery/',OrderDeliveryCreateView.as_view(),name='order-delivery'),
    path('order/<int:pk>/payment/', PaymentCreateView.as_view(), name='order-payment-create'),
    path('order/<int:pk>/progress', PaymentSuccessView.as_view(), name='progress'),
    path('order/<int:pk>/progress', PaymentSuccessView.as_view(), name='progress'),
    path('order/<int:pk>/cartdetail', OrderCartDetailView.as_view(), name='order-cart'),

    path('order/<int:pk>/payment', OrderPaymentDetailView.as_view(), name='order-payment'),

]