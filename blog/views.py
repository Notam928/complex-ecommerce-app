from django.shortcuts import render
from django.views.generic import TemplateView

class BlogView(TemplateView):
    """
    Blog view
    
    """
    template_name = "blog/blog.html"
