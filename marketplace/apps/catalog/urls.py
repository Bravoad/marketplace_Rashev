from django.urls import path
from .views import AboutView,IndexView,CatalogView,CategoryCatalogView,ProductDetailView,CatalogOrderReviewsView,SaleView,SaleDetailView,CatalogOrderPriceView,CatalogOrderNewView
urlpatterns = [
    path('', IndexView.as_view(), name='main'),

    path('about', AboutView.as_view(), name='about'),
    path('catalog', CatalogView.as_view(), name='catalog-list'),
    path('sale', SaleView.as_view(), name='sale-list'),

    path('catalog', CatalogOrderReviewsView.as_view(), name='catalog-reviews'),
    path('catalog', CatalogOrderNewView.as_view(), name='catalog-new'),
    path('catalog',CatalogOrderPriceView,name='catalog-price'),
    path('catalog/<str:slug>', CategoryCatalogView.as_view(), name='catalog_category'),
    path('catalog/<str:slug>', ProductDetailView.as_view(), name='catalog_detail'),
]
