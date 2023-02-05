from django.urls import path
from .views import OrderDetailView,OrderCreateView,OrderListView

urlpatterns = [
    path('order',OrderListView.as_view(),name='order-list'),
    path('order/<int:pk>',OrderDetailView.as_view(),name='order-detail'),
    path('order-create',OrderCreateView.as_view(),name='order-create'),
]