from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from accounts.models import User

class Category(models.Model):
    """
    Category model for manage category field
    
    :Attributes
      - image: is require because the design
      - name: name of category
      - created_at: date and time of creation
      - updated_at: data and time of updating
    """
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="upload/category/")
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
    def et_absolute_url(self):
        return reverse("core:category", kwargs={"pk": self.pk})
    
    
        
class Tag(models.Model):
    """
    Tag class is model who manage tag ressource
        Attributes:
        - name: The name of tag
    """
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("core:tags", kwargs={"pk": self.pk})
    


class ProductImage(models.Model):
    """
    Image of product 
    
    :Atributtes
        -product: the current product 
        -images: all images of product
      
    """
    product = models.ForeignKey(
        "Product", 
        default=None, 
        on_delete=models.CASCADE
    )
    images = models.FileField(upload_to ='upload/products/')
    
    def __str__(self):
        return self.product.name



class Product(models.Model):
    """
    Post model for manage the product of ecommerce app
    
    :Attributes
      -name: product name
      -color: the product color
      -image: the product image
    """
    #color
    BLUE = "b"
    WHITE = "w"
    RED = "r"
    GREEN = "g"
    BLACK = "bl"
    UNDEFIND = "u"
    
    #sizes
    SMALL = "s"
    MEDUIM = "m"
    LARGE = "l"
    X_SMAILL = "xs"
    
    COLOR_PRODUCT = [
        (BLUE, "Blue"), 
        (WHITE, "White"),
        (RED, "Red"),
        (GREEN, "Green"),
        (BLACK,"Black"),
    ]
    
    SIZE_CHOICES = [
        (SMALL, "S"),
        (MEDUIM, "M"),
        (LARGE,"L"),
        (X_SMAILL, 'XS')
    ]
    
    
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to="upload/products")
    description = models.CharField(max_length=300)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    color = models.CharField(max_length=3, choices=COLOR_PRODUCT, default=UNDEFIND)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default=SMALL)
    category = models.ForeignKey(
        Category, 
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    tag = models.ManyToManyField(Tag, related_name="tags", blank=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    
    
    
    def get_absolute_url(self):
        # absolute url
        return reverse("core:product", kwargs={"slug":self.slug})
    
    

