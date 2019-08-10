"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sign import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('event_manage/', views.event_manage, name='event_manage'),
    path('guest_manage/', views.guest_manage, name='guest_manage'),
    path('serach_name/', views.event_serach_name, name='event_serach_name'),
    path('guest_serach_name/', views.guest_serach_name, name='guest_serach_name'),
    path('sign_index/<int:event_id>/', views.sign_index, name='sign_index'),
    path('sign_index_action/<int:event_id>/', views.sign_index_action, name='sign_index_action'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('add_event/', views.add_event, name='add_event'),
    path('logout/', views.logout, name='logout'),
]
