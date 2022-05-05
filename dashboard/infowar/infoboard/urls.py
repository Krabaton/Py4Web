from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('typelosses/', views.create_type, name='typelosses'),
    path('losses/actual', views.get_losses_actual, name='actuallosses'),
    path('losses/list', views.losses_list, name='losseslist'),
    path('sync/', views.sync_losses, name='lossessync'),
    path('chart/<int:id>', views.get_chart, name='getchart'),
    path('chart-info/<int:id>', views.get_chart_info, name='getchartinfo')
]
