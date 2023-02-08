from django.urls import path
from .views import CartView,CartAddView,CartRemoveView
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:product>/add/', CartAddView.as_view(), name='cart_add'),
    path('<int:product>/remove/', CartRemoveView.as_view(), name='cart_remove'),
]
