from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,UpdateView,FormView,View,DetailView,ListView,CreateView
from .models import Product,Category,Review,Sale,Attributes,Gallery,Tags
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
        context['limited_catalog'] = Product.objects.select_related('category').filter(is_limited=True).all()[:16]
        context['popular_catalog'] = Product.objects.select_related('category').filter(is_popular=True).all()[:16]
        context['banner_catalog'] = Product.objects.select_related('category').filter(is_banner=True).all().order_by('price')[:16]
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
        context['catalog'] = Product.objects.filter(count__gt=0,category=self.object)
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product.html'

    def get(self, request, *args, **kwargs):
        viewed_list = Viewed_list(self.request)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        viewed_list.add(product=self.object)
        context['reviews'] = Review.objects.filter(product_id=self.object)
        context['attributes'] = Attributes.objects.filter(product_id=self.object)
        context['tags'] = Tags.objects.filter(product_id=self.object)
        context['gallery'] = Gallery.objects.filter(product_id=self.object).first()
        context['galleries'] = Gallery.objects.filter(product_id=self.object).all()[1::]
        return self.render_to_response(context)


class ReviewWithoutUsernameCreateView(View):

    def post(self, request,**kwargs):
        product = Product.objects.get(pk=self.kwargs['pk'])
        user = User.objects.get(pk=self.request.user.id)
        comment = self.request.POST.get('review')
        Review.objects.create(user=user, comment=comment,product=product).save()
        return reverse('product_detail',kwargs={'pk':self.kwargs['pk']})


class SaleView(TemplateView):
    template_name = 'pages/sale.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = Sale.objects.all()
        return context


class ViewedListView(TemplateView):
    template_name = 'pages/viewed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['viewed_list'] = Viewed_list(self.request)
        return context


class ViewedRemoveView(View):

    def get(self,request,**kwargs):
        viewed = Viewed_list(self.request)
        pk = self.kwargs['product']
        product = get_object_or_404(Product, id=pk)
        viewed.remove(product=product)
        return redirect('viewed')


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'pages/product.html'


class CatalogOrderReviewsView(ListView):
    template_name = 'pages/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.annotate(reviews=Count('review')).order_by('reviews')
        return context


class CatalogOrderNewView(ListView):
    template_name = 'pages/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.order_by('-created')
        return context


class CatalogOrderPriceView(ListView):
    template_name = 'pages/catalog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.order_by('price')
        return context


class CatalogSearchView(ListView):
    model = Product
    template_name = "pages/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context['catalog'] = Product.objects.filter(name__icontains=query).all()
        return context
