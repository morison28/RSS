from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'rss_app'

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('add/', views.addfeed_view, name='add'),
    path('feed/<path:site_feed_url>/', views.feed_view, name='feed'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('favorite/', views.favorite_view, name='favorite'), 
    path('add_favorite/<path:article_url>/<path:article_title>', views.add_favorite, name='add_favorite'),
    path('delete_favorite/<path:article_url>/<path:article_title>', views.delete_favorite, name='delete_favorite'),
]
