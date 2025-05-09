from django.contrib import admin
from .models import Product, Message, Order, OrderItem, Image, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Message)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Image)
admin.site.register(Review)