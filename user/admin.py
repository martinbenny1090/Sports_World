from django.contrib import admin
from .models import Order, OrderItem, Item, Contact
# Register your models here.

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Contact)