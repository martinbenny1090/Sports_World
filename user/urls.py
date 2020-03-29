from django.urls import path
from . import views 
from user.views import HomeView, ItemDetailView
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('offer', views.offer),
    path('about', views.about),
    path('contact', views.contact),
    # path('owner', views.owner, name="owner"),
    path('add-to-cart/<slug>', views.add_to_cart, name="add-to-cart")

]