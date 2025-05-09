from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.
    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Surfboards", "Surfboards"),
        ("Skimboards", "Skimboards")
    ]

    name = models.CharField(max_length=75)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    originalPrice = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    description = RichTextField()
    cogs = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0)

    def __str__(self):
        return f"{self.id} - {self.name}"

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.CharField(max_length=250)

    def __str__(self):
        return f"Image for {self.product.name}"

class Message(models.Model):
    sender = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} - {self.subject}"

class Order(models.Model):
    STATUS_CHOICES = [
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancelled")
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    shippingMethod = models.CharField(max_length=50, default="Standard")
    trackingNumber = models.CharField(max_length=100, null=True, blank=True, default=None)
    products = models.ManyToManyField(Product, through='OrderItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return f"{self.name} - {self.status}" 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order: {self.order.id} - {self.product} x{self.quantity}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review = models.CharField(max_length=10000)

    def __str__(self):
        return f"{self.product} rating: {self.rating}"