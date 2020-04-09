from django.contrib import admin
from .models import Order, OrderItem, Item, Contact, BillingAddress, Payment
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'billing_address',
        'payment' ]
    list_display_links = [
        'user',
        'billing_address',
        'payment'
    ]
    list_filter =[
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Contact)
admin.site.register(BillingAddress)
admin.site.register(Payment)