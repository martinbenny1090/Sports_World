from django.contrib import admin
from .models import Order, OrderItem, Item, Contact, BillingAddress, Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Contact)
admin.site.register(BillingAddress)
admin.site.register(Payment)