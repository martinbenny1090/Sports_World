from django.urls import path
from . import views 
# from user.views import HomeView, ItemDetailView


urlpatterns = [
    path('', views.home , name='home'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('Register', views.register, name="register"),
    # path('product', ItemDetailView.as_view(), name='product'),
    path('offer', views.offer),
    path('about', views.about),
    path('contact', views.contact),
    # path('owner', views.owner, name="owner"),

]