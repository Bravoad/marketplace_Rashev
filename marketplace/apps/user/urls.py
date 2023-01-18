from django.urls import path
from .views import IndexView,AuthView,LogView,RegisterUser,UserDetailView
urlpatterns = [
    path('', IndexView.as_view(), name='account'),
    path('login/', AuthView.as_view(), name='log-in'),
    path('logout/', LogView.as_view(), name='log-out'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
#    path('profile/<int:pk>/add_balance', BalanceView.as_view(), name='add-balance'),

]
