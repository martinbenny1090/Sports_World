from django.urls import path
from . import views


urlpatterns = [
    path('', views.owhome, name="owhome"),

]