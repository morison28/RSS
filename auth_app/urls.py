from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'auth_app'

urlpatterns = [
    path('signup/', views.signupfunc, name='signup'),
    path('login/', views.loginfunc, name='login'),
    path('logout/', views.logoutfunc, name='logout'),
]