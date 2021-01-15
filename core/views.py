from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

from core.models import (
    Product, ProductImage,Category, Tag, Order,OderItem, Payment, 
    Address, Coupon
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


class OrderSummaryView(LoginRequiredMixin, View):
    
    """
    Display the user cart 
    """
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            return render(self.request, "core/checkout.html", context=context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    #get current product
    product = get_object_or_404(Product, slug=slug)
    #get or add product to item
    order_item, created = OderItem.objects.get_or_create(
        item = product,
        user = request.user,
        ordered = False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            #update order item
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This product quantity was updated")
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Tis product was added to your cart")
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Oder.objects.create(user=request.user, ordered_date= ordered_date)
        order.items.add(order_item)
        messages.info(request, "This product added to your cart")
        return redirect("core:order_summary")
            
    
    
    