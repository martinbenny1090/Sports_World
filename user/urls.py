from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('Register', views.register, name="register"),
    path('product', views.product),
    path('offer', views.offer),
    path('about', views.about),
    path('contact', views.contact),
    # path('owner', views.owner, name="owner"),

]