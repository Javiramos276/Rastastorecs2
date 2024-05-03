from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import Arma

# Create your views here.

class ItemsView(TemplateView):
    model = Arma
    template_name = "home.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['armas'] = Arma.objects.all()
        return context
    
    def get_queryset(self):
        categoria = self.kwargs.get('categoria')
        return Arma.objects.filter(categoria=categoria)
    

class FiltrarArmasListView(ListView):
    template_name = 'home.html'
    context_object_name = 'armas'
    
    def get_queryset(self):
        categoria = self.kwargs.get('categoria')
        if categoria:
            return Arma.objects.filter(categoria=categoria)
        else:
            return Arma.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = self.kwargs.get('categoria')
        return context   
    
