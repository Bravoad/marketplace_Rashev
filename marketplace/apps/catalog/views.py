from django.contrib.auth.models import User
from django.db.models import Count,Max,Min
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,UpdateView,FormView,View,DetailView,ListView,CreateView
from .models import Product,Category,Review,Sale,Attributes,Gallery,Tags
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
    model = Product
    template_name = 'pages/catalog.html'
    queryset = Product.objects.all()
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog']= Product.objects.all()
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()

        return context


class CategoryCatalogView(DetailView):
    model = Category
    template_name = 'pages/catalog.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['catalog'] = Product.objects.filter(count__gt=0,category=self.object)
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)

        return self.render_to_response(context)


class TagsCatalogView(DetailView):
    model = Tags
    template_name = 'pages/catalog.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['catalog'] = Product.objects.filter(count__gt=0,tags=self.object)
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['reviews'] = Review.objects.filter(product_id=self.object)
        context['attributes'] = Attributes.objects.filter(product_id=self.object)
        context['tags'] = Tags.objects.filter(product_id=self.object)
        context['gallery'] = Gallery.objects.filter(product_id=self.object).first()
        context['galleries'] = Gallery.objects.filter(product_id=self.object).all()[1::]
        return self.render_to_response(context)


class ReviewWithoutUsernameCreateView(View):

    def post(self, request,**kwargs):
        product = Product.objects.get(pk=int(self.kwargs['pk']))
        user = User.objects.get(pk=self.request.user.id)
        comment = self.request.POST.get('review')
        Review.objects.create(user=user, comment=comment,product=product).save()
        return redirect(self.request.META['HTTP_REFERER'])


class SaleView(ListView):
    model = Sale
    template_name = 'pages/sale.html'
    paginate_by = 10
    queryset = Sale.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales'] = Sale.objects.all()
        return context


class SaleDetailView(DetailView):
    model = Sale
    template_name = 'pages/sale_detail.html'
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CatalogOrderReviewsView(ListView):
    template_name = 'pages/catalog.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.annotate(reviews=Count('review')).order_by('reviews')
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return context


class CatalogOrderNewView(ListView):
    template_name = 'pages/catalog.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.order_by('-created')
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return context


class CatalogOrderPopularView(ListView):
    model = Product
    template_name = 'pages/catalog.html'
    queryset = Product.objects.all()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.order_by('-is_popular')
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return context

class CatalogOrderPriceView(ListView):
    model = Product
    template_name = 'pages/catalog.html'
    queryset = Product.objects.all()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = Product.objects.order_by('price')
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return context


class CatalogSearchView(ListView):
    model = Product
    template_name = "pages/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context['catalog'] = Product.objects.filter(name__icontains=query).all()
        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)

        return context


class CatalogFilter(ListView):
    model = Product
    template_name = "pages/catalog.html"
    queryset = Product.objects.all()
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        price = self.request.GET.get("price")
        name = self.request.GET.get("name")
        aviable = self.request.GET.get("aviable")
        delivery = self.request.GET.get("delivery")
        if price:
            context['catalog'] = Product.objects.filter(price__range=[int(i) for i in price.split(';')]).all()
        if name:
            context['catalog'] = Product.objects.filter(name__icontains=name).all()
        if aviable:
            context['catalog'] = Product.objects.filter(count__gte=0).all()
        if delivery:
            context['catalog'] = Product.objects.filter(is_free_delivery=True).all()

        context['min_price'] = Product.objects.order_by('price').first()
        context['max_price'] = Product.objects.order_by('-price').first()
        context['tags'] = Tags.objects.filter(is_popular=True)
        return context
