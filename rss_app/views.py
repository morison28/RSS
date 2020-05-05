from django.shortcuts import render, redirect
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import Feed, Favorite 

import feedparser

User = get_user_model()
feed = Feed()
#favorite = Favorite()

# Create your views here.


def homefunc(request):
    print('ホームに移動')
    objects = Feed.objects.filter(user_id=request.user.id)
    print(objects)
    print(request.user.email)
    #print('ユーザーID', request.user.id)
    #print('プリントURL：',objects[0].feed_url)
    #print('TYPE:', type(objects[0].feed_url))
    # print(objects)
    # print(len(objects))
    # print(objects[0])
    # print(objects[0].feed_url)

    #entries = feedparser.parse(url).entries
    entries = []
    for obj in objects:
        url = obj.feed_url
        etr = feedparser.parse(url).entries
        entries.append(etr)
    # print(type(entries[0]))
    # print(len(entries))
    context = {
        'objects': objects,
        #'o': objects[0],
        'username': request.user.email,
        'entries_lst': entries,
    }
    
    return render(request, 'home.html', context)


def dashboard_view(request):
    print('ダッシュボードに移動')
    objects = Feed.objects.filter(user_id=request.user.id)
    #print('プリントURL：',objects[0].feed_url)
    #print('TYPE:', type(objects[0].feed_url))
    #print(objects)
    #for k,v in objects:
        #objects[k]['feed_url_str'] = objects[k].feed_url.replace('/', '%')
    entries = []
    for obj in objects:
        url = obj.feed_url
        etr = feedparser.parse(url).entries
        entries.append(etr)
    context = {
        'objects': objects,
        'username': request.user.email,
        'entries_lst': entries,
    }
    return render(request, 'dashboard.html', context)

def all_articles_view(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    context = {
        'objects': objects
    }
    return render(request, 'all_articles.html', context)

def welcomefunc(request):
    return render(request, 'welcome.html')


def signupfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'signup.html', {'error': 'このユーザーは登録されています'})
        except:
            # user登録ができたらログインページ移行する
            user = User.objects.create_user(email=email, password=password)
            return render(request, 'login.html')
            
    return render(request, 'signup.html')


def loginfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('rss_app:home')
        else:
            return redirect('rss_app:welcome')
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('rss_app:welcome')

def addfeedfunc(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    print('追加前', Feed.objects.filter(user_id=request.user.id))
    if request.method == 'POST':
        url = request.POST['url']
        data = Feed(title=feedparser.parse(url)['feed']['title'],
                    user_id=request.user.id,
                    feed_url=url,
                    feed_url_str=url.replace('/','%'))
        data.save()
        print('ユーザID', request.user.id, 'に追加しました')
        print('added_feed =', url)
        print('追加後', Feed.objects.filter(user_id=request.user.id))
        return render(request, 'home.html', {'objects':objects})
    return render(request, 'add.html', {"objects":objects})


def feed_view(request, param):
    print('フィード関数が呼び出されたよ')
    """
    feed_url_strのようなものを定義し、モデルに追加
    使用するときにはreplaceして利用する
    """
    print(param)
    print(Feed.objects.filter(feed_url_str=param))
    obj = Feed.objects.filter(feed_url_str=param)[0]
    objects = Feed.objects.filter(user_id=request.user.id)
    print('オブジェクト', obj)
    print('オブジェクトタイプ', type(obj))
    url = str(obj)
    print('URL', url)
    print('URLタイプ', type(url))
    entries = feedparser.parse(url).entries

    users_favorite_list = list(Favorite.objects.filter(user=request.user))
    users_favorite_list = list(map(lambda x: str(x), users_favorite_list))

    context = {
        'objects': objects,
        'entries': entries,
        'users_favorite_list': users_favorite_list,
    }
    return render(request, 'feed.html', context)


def add_favorite(request, prm, param):
    objects = Feed.objects.filter(user_id=request.user.id)

    #print(objects)

    users_favorite_queryset = Favorite.objects.filter(user=request.user)
    users_favorite_list = list(Favorite.objects.filter(user=request.user))
    """
    print(users_favorite_queryset)
    print(users_favorite_list)
    print(type(users_favorite_list))
    print(prm)
    """
    for i in users_favorite_list:
        print(i)
    unique = True
    for added_title in users_favorite_list:
        added_title = str(added_title)
        if added_title == prm:
            unique = False
            break
    if unique:
        
        data = Favorite(user_id=request.user.id,
                        favorite_article_title = prm,
                        favorite_article_url = param 
                        )
        data.save()
        
        print('お気に入りに追加しました')

    d = {
        'SomeData': 100
    }
    return  HttpResponse(d)#render(request, 'favorite.html')#redirect('dashboard')#JsonResponse(d)#HttpResponse('') #redirect(request.META['HTTP_REFERER'])#reverse('feed') 

def delete_favorite(request):
    return HttpResponse('delete')

def favorite_view(request):
    objects = Feed.objects.filter(user_id=request.user.id)
    favorite = Favorite.objects.filter(user=request.user)
    #print(favorite)
    context = {
        'objects': objects,
        'favorite': favorite,
    }
    return render(request, 'favorite.html', context)



