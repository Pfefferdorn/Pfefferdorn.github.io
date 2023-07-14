from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', index),
    path('remove/<str:city>/', views.remove_city, name='remove_city')
]
