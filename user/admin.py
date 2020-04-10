from django.contrib import admin
from .models import Order, OrderItem, Item, Contact, BillingAddress, Payment, Refund
# Register your models here.

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_granted=True)


make_refund_accepted.short_description = 'Update refund requested to refund granted'

def remove_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_granted=False)


remove_refund_accepted.short_description = 'Remove refund granted to not'


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
    actions = [make_refund_accepted, remove_refund_accepted]


class BillingAddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Contact)
admin.site.register(BillingAddress, BillingAddressAdmin)
admin.site.register(Payment)
admin.site.register(Refund)