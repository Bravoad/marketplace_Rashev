from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,UpdateView,FormView,View,DetailView,ListView,CreateView
from .models import Product,Category,Review,Sale,Attributes
from .forms import CartAddProductForm,ReviewWithoutUsernameForm
from .viewed_list import Viewed_list
from django.urls import reverse, reverse_lazy

# Create your views here.


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IndexView(TemplateView):
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limited_catalog'] = Product.objects.select_related('category').filter(count__lt=100,available=True)
        context['popular_catalog'] = Product.objects.select_related('category').filter(is_popular=True,available=True)
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product.html'

    def get(self, request, *args, **kwargs):
        viewed_list = Viewed_list(self.request)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        viewed_list.add(product=self.object)
        if self.request.user.is_authenticated:
            context['form'] = ReviewWithoutUsernameForm()
        context['reviews'] = Review.objects.filter(product_id=self.object)
        context['attributes'] = Attributes.objects.filter(product_id=self.object)
        return self.render_to_response(context)


class ReviewWithoutUsernameCreateView(CreateView):
    form_class = ReviewWithoutUsernameForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('product-detail', kwargs={'pk': pk})

    def form_valid(self, form):
        news = Product.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=self.request.user.id)
        form.instance.news = news
        form.instance.author = user
        form.instance.username = user.username
        return super().form_valid(form)


class SaleView(ListView):
    template_name = 'pages/sale.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale']= Sale.objects.all()
        return context


class ViewedListView(TemplateView):
    template_name = 'pages/viewed.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewed_list'] = Viewed_list(self.request)
        return context


class ViewedRemoveView(FormView):

    def form_valid(self, form):
        viewed = Viewed_list(self.request)
        pk = self.kwargs['product']
        product = get_object_or_404(Product, id=pk)
        viewed.remove(product=product)
        return redirect('cart_detail')
