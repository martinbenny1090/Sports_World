from django.urls import path
from . import views 
from user.views import HomeView, ItemDetailView

app_name = 'user'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('Register', views.register, name="register"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('offer', views.offer),
    path('about', views.about),
    path('contact', views.contact),
    # path('owner', views.owner, name="owner"),
    # 'products/<int:myid>'

]