from django.shortcuts import render
from django.views.generic import View, ListView, DetailView

from core.models import (
    Category, ProductImage, Product
)

class HomeView(View):
    #Home view baseon class
    
    def get(self, *args, **kwargs):
        
        # query with django ORM
        context = {
            "categories": Category.objects.all(),
            "products": Product.objects.all(),
        }
        
        return render(self.request,"core/index.html", context=context)
    
    
    

class ShopView(ListView):
    """
    CBV for shop: display all post by pagination
    """
    model = Product
    template_name ="core/shop.html"
    paginate_by = 50




class ProductDetail(DetailView):
    """
    Detail view
    """
    model = Product
    template_name = "core/product.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] =  ProductImage.objects.filter(product=self.get_object())
        return context
    