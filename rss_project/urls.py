from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rss_app.urls')),
    path('rss/', include('auth_app.urls')),
]
