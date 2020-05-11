from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import Feed, Favorite 

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('rss_app/views.py')
import feedparser

User = get_user_model()
feed = Feed()

# Create your views here.

@login_required
def dashboard_view(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    entries = []
    for obj in objects:
        url = obj.feed_url
        etr = feedparser.parse(url).entries
        entries.append(etr)
    context = {
        'objects': objects,
        'username': request.user.email
    }
    return render(request, 'rss_app/dashboard.html', context)


def welcome_view(request):
    return render(request, 'rss_app/welcome.html')


@login_required
def addfeed_view(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        url = request.POST['url']
        entries = feedparser.parse(url)['entries']
        if entries:
            feed = Feed(
                title=feedparser.parse(url)['feed']['title'],
                user_id=request.user.id,
                feed_url=url,
                feed_url_str=url.replace('/','%')
            )
            feed.save()
            return render(request, 'home.html', {'objects':objects})
        else:
            context = {
                'objects': objects,
                'message': '*有効なURLを入力してください'
            }
            return render(request, 'rss_app/add.html', context)
    return render(request, 'rss_app/add.html', {"objects":objects})

@login_required
def feed_view(request, site_feed_url):
    obj = Feed.objects.filter(feed_url_str=site_feed_url)[0]
    objects = Feed.objects.filter(user_id=request.user.id)
    url = str(obj)
    entries = feedparser.parse(url).entries

    users_favorite_list = list(Favorite.objects.filter(user=request.user))
    users_favorite_list = list(map(lambda x: str(x), users_favorite_list))

    context = {
        'objects': objects,
        'entries': entries,
        'users_favorite_list': users_favorite_list,
    }
    return render(request, 'rss_app/feed.html', context)


def add_favorite(request, article_title, article_url):
    objects = Feed.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        users_favorite_queryset = Favorite.objects.filter(user=request.user)
        users_favorite_list = list(Favorite.objects.filter(user=request.user))
    
        unique = True
        for added_title in users_favorite_list:
            added_title = str(added_title)
            if added_title == article_title:
                unique = False
                break
        if unique:
            favorite = Favorite(
                user_id=request.user.id,
                favorite_article_title = article_title,
                favorite_article_url = article_url,
            )
            favorite.save()

        return  HttpResponse('add_favorite')

def delete_favorite(request,article_title,article_url):
    if request.method == 'POST':
        delete_target = Favorite.objects.filter(user=request.user).get(favorite_article_title=article_title)
        Favorite.objects.filter(user=request.user).get(favorite_article_title=article_title).delete()
        #users_favorite_queryset = Favorite.objects.filter(user=request.user)
        logger.debug('deleted: %s', delete_target)
        return HttpResponse('delete_favorite')

@login_required
def favorite_view(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    favorite = Favorite.objects.filter(user=request.user)
    context = {
        'objects': objects,
        'favorite': favorite,
    }
    return render(request, 'rss_app/favorite.html', context)




