from django.urls import path
from .views import AuthView,LogView,RegisterUser,UserDetailView,EditUser,RegisterCartUser,CreateUser,CreateCartUser
urlpatterns = [
    path('login/', AuthView.as_view(), name='log-in'),
    path('logout/', LogView.as_view(), name='log-out'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('register-user-order/', RegisterCartUser.as_view(), name='register-user-order'),
    path('create/',CreateUser.as_view(), name='create-user'),
    path('create-user-order/', CreateCartUser.as_view(), name='create-user-order'),

    path('profile/<int:pk>', UserDetailView.as_view(), name='account'),
    path('profile/<int:pk>/edit', EditUser.as_view(), name='edit'),
]
