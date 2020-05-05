from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'rss_app'

urlpatterns = [
    # to signin & login
    path('', views.welcomefunc, name='welcome'),
    path('home/', views.homefunc, name='home'),
    #path('dashboard/', views.dashboardfunc, name='dashboard), 
    path('signup/', views.signupfunc, name='signup'),
    #path('signup_done/', views.signup_done_view, name='signup_done'),
    #path(''),
    path('login/', views.loginfunc, name='login'),
    #path('search/', views.searchfunc, name='search'),
    path('add/', views.addfeedfunc, name='add'),
    path('feed/<path:param>/', views.feed_view, name='feed'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('all_articles/', views.all_articles_view, name='all_articles'),
    path('favorite/', views.favorite_view, name='favorite'), # お気に入り記事は別のデータベースで作成し、Userごとのページをこしらえる必要がある
    path('add_favorite/<path:param>/<path:prm>', views.add_favorite, name='add_favorite'),
    path('delete_favorite/<path:param>/<path:prm>', views.delete_favorite, name='delete_favorite')


]
