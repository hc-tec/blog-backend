from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('main/', include('main.urls')),
    path('websocket/', include('chat.urls')),
]
