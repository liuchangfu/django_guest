from django.contrib import admin
from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('add_event/', views.add_event, name='add_event'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('get_event_list/', views.get_event_list, name='get_event_list'),
    path('get_guest_list/', views.get_guest_list, name='get_guest_list'),
    # path('user_sign/', views.user_sign, name='user_sign'),
]
