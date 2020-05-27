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


class paymentFilters(django_filters.FilterSet):
    start_date=DateFilter(field_name="timestamp",lookup_expr='gte')
    end_date=DateFilter(field_name="timestamp",lookup_expr='lte')
    class Meta:
        model = Payment 
        fields = '__all__'
        exclude = ['stripe_charge_id','amount','timestamp']

class orderitemsFilters(django_filters.FilterSet):
    start_date=DateFilter(field_name="AddedDate",lookup_expr='gte')
    end_date=DateFilter(field_name="AddedDate",lookup_expr='lte')
    class Meta:
        model = OrderItem 
        fields = '__all__'
        exclude = ['ordered','item','quantity','AddedDate', 'order_id']