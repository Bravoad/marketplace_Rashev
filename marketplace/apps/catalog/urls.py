from django.urls import path
from .views import AboutView,IndexView
urlpatterns = [
    path('', IndexView.as_view(), name='main'),

    path('about', AboutView.as_view(), name='about'),

]
