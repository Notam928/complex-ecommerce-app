
from django.contrib import admin
 
from core.models import (
    Product, ProductImage,Category, Tag
    )
 
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
 
 
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin,]
    prepopulated_fields = {"slug": ("name",)}
    
    class Meta:
       model = Product
 

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
