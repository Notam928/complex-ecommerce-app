from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    #Home view baseon class
    
    template_name = "core/index.html"
    
    
