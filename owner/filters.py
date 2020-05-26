import django_filters
from django_filters import DateFilter

from user.models import *

class OrderFilters(django_filters.FilterSet):
    start_date=DateFilter(field_name="ordered_date",lookup_expr='gte')
    end_date=DateFilter(field_name="ordered_date",lookup_expr='lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['ordered_date','ref_code', 'user', 'items', 'ordered', 'billing_address', 'payment', 'being_delivered', 'received', 'refund_requested', 'refund_granted']