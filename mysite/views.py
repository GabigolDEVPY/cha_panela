from django.shortcuts import render
from . models import Items
from django.views.generic import TemplateView
# Create your views here.

class Home(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Items.objects.filter(active=True)
        return context
    
    