from django.urls import path
from . import views 
from  user.views import HomeView, ItemDetailView

app_name = 'user'
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('checkout', views.checkout, name="checkout"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>', views.add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>', views.remove_from_cart, name="remove-from-cart")
   
]