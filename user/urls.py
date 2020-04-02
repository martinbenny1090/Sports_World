from django.urls import path
from . import views 
from  user.views import HomeView, ItemDetailView, OrderSummaryView

app_name = 'user'
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('checkout', views.checkout, name="checkout"),
    path('order-summary', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', views.remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>', views.remove_single_item_from_cart, name="remove-single-item-from-cart"),
    path('contact', views.contact, name="contact")
    
   
]