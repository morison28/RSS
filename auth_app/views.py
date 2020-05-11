from django.shortcuts import render, redirect
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import JsonResponse
#from .models import Feed, Favorite 

# Create your views here.
def test_view(request):
    return HttpResponse('<h1>auth_app test page</h1>')


def signupfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'auth_app/signup.html', {'error': 'このユーザーは登録されています'})
        except:
            # user登録ができたらログインページ移行する
            user = User.objects.create_user(email=email, password=password)
            return render(request, 'auth_app/login.html')
            
    return render(request, 'auth_app/signup.html')

def loginfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('rss_app:dashboard')
        else:
            return redirect('rss_app:welcome')
    return render(request, 'auth_app/login.html')

def logoutfunc(request):
    logout(request)
    return redirect('rss_app:welcome')