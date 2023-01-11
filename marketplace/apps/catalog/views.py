from django.shortcuts import render
from django.views.generic import TemplateView,UpdateView,FormView,View
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
        return context
