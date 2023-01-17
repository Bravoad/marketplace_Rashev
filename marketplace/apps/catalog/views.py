from django.shortcuts import render
from django.views.generic import TemplateView,UpdateView,FormView,View,DetailView,ListView
from .models import Product,Category,Review,Seller,Sale
from .viewed_list import Viewed_list
#Create your views here.


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limited_catalog'] = Product.objects.select_related('seller', 'category').filter(count__lt=100,available=True)
        context['popular_catalog'] = Product.objects.select_related('seller', 'category').filter(is_popular=True,available=True)
        context['banner_catalog'] = Product.objects.only('name', 'is_banner', 'category__slug', 'image','price').filter(available=True, is_banner=True)
        return context


class CatalogView(ListView):
    template_name = 'pages/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog']= Product.objects.all()
        return context

class CategoryCatalogView(DetailView):
    model = Category
    template_name = 'pages/catalog.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['catalog'] = Product.objects.filter(count__gt=0,category__slug=self.object.slug).all()
        return self.render_to_response(context)
