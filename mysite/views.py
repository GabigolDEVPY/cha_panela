from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Home(TemplateView):
    template_name = "index.html"
    
    def get_queryset(self):
        return super().get_queryset()
    