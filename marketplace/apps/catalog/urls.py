from django.urls import path
from .views import AboutView,IndexView,CatalogView,CategoryCatalogView,ProductDetailView,CatalogOrderReviewsView,SaleView,SaleDetailView,CatalogOrderPriceView,CatalogOrderNewView,\
    CatalogSearchView, ViewedListView,ReviewWithoutUsernameCreateView
urlpatterns = [
    path('', IndexView.as_view(), name='main'),

    path('about', AboutView.as_view(), name='about'),
    path('catalog', CatalogView.as_view(), name='catalog-list'),
    path('sale', SaleView.as_view(), name='sale-list'),
    path('sale/<str:slug>', SaleDetailView.as_view(), name='sale-detail'),

    path('catalog/rev', CatalogOrderReviewsView.as_view(), name='catalog-reviews'),
    path('catalog/new', CatalogOrderNewView.as_view(), name='catalog-new'),
    path('catalog/price',CatalogOrderPriceView,name='catalog-price'),
    path('catalog/category/<str:slug>', CategoryCatalogView.as_view(), name='catalog_category'),
    path('catalog/product/<str:slug>', ProductDetailView.as_view(), name='catalog_detail'),
    path('catalog/product/<int:pk>/review/', ReviewWithoutUsernameCreateView.as_view(), name='catalog_review'),
    path('catalog/product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),

    path('catalog/search/', CatalogSearchView.as_view(), name='catalog-search'),
    path('viewed', ViewedListView.as_view(), name='viewed'),

]
