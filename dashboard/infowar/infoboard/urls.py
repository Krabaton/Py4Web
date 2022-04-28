from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('typelosses/', views.create_type, name='typelosses'),
]
