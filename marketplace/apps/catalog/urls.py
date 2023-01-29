from django.urls import path
from .views import AboutView,IndexView,CatalogView,CategoryCatalogView,ProductDetailView
urlpatterns = [
    path('', IndexView.as_view(), name='main'),

    path('about', AboutView.as_view(), name='about'),
    path('catalog', CatalogView.as_view(), name='catalog-list'),
    path('catalog/<str:slug>', CategoryCatalogView.as_view(), name='catalog_category'),
    path('catalog/<str:slug>', ProductDetailView.as_view(), name='catalog_detail'),

]
