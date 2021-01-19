from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from django_countries.fields import CountryField

from accounts.models import User



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


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



class OderItem(models.Model):
    """
    Manage the order item
    
    Atributtes
        - user: User request the order 
        - ordered: True or False, check if comment is pay
        - item: the product relative in order
        - qauntity: Product quantity
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
    
    def get_total_item_price(self):
        # the total price of an product with the number of this quantity
        return self.quantity * self.item.price
    
    def get_total_discount_price(self):
        # the total price of a product with the number of this quantity and discount_price
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        #amount  of product (price - discount_priec)
        return self.get_total_item_price() - self.get_total_discount_price()
        
    def get_final_price(self):
        #the final price of order Item
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price
    
    
class Order(models.Model):
    """
    Manage the user order 
    
    Atributtes
        - user: the user who send order
        - items: the differents product in order
        - start_date: the date commande start
        - ordered: status of pay or not
        - shipping_address: shipping address 
        - billing_address: blling address
        - payment: payement method
        - coupon: coupon
        - being_delivered : command being delivered 
        - received: command is received by user 
        - refund_granted: refund granted by user 
        - refund_requested: refund requested by user 
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        "Address", 
        related_name='shipping_address', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    billing_address = models.ForeignKey(
        "Address", 
        on_delete=models.SET_NULL,
        related_name='billing_address', 
        blank=True, 
        null=True
    )
    payment = models.ForeignKey("Payment", on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey("Coupon", on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    
    def get_total(self):
        # get the total price in order
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        # withdraw  coupon if exist
        if self.coupon:
            total -= self.coupon.amount
        
        return total
            
    
    

class Address(models.Model):
    """
    Manage the address
    
    Atributtes:
        - user: the user to whom the address belongs
        - street_address: address
        - apartment_address: delievery apartment
        - country:  user's country
        - code_zip:  code zip
        - address_type: 
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    code_zip = models.CharField(max_length=120)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    
    class Meta:
        verbose_name_plural = "Addresses"
        


    
class Payment(models.Model):
    """
    Manage the payment model
    
    Atributtes:
        - stripe_charge_id : strip charge id when user checkout
        - user: the user who checkout
        - amount: payment amount 
        - created_at: data and time of payment
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    stripe_charge_id = models.CharField(max_length=50) 
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name


class Coupon(models.Model):
    """
    Manage the coupon model
    
    Atributtes:
        - code : coupon code
        - amount:  the amount 
    """
    code = models.CharField(max_length=5)
    amount = models.FloatField()
    
    def __str__(self):
        return self.code
    
    
class Refund(models.Model):
    """
    Manage the refund model
    
    Atributtes:
        - order: the relatif order
        - reason: The raison of development 
        - acepted: boolean for check if refund is acepte
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    acepted = models.BooleanField(default=False)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.pk}"
    
    
    
    
    
    
    

