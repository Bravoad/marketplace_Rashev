from django.urls import path
from .views import CartView,CartAddView,CartRemoveView
urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('cart/<int:product>/add', CartAddView.as_view(), name='cart_add'),
    path('cart/<int:product>/remove', CartRemoveView.as_view(), name='cart_remove'),

    path('', CartView.as_view(), name='cart'),

]
