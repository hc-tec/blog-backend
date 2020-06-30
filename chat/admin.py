from django.contrib import admin
from .models import (ChatInfo, ChatRoom)


admin.site.register(ChatRoom)
admin.site.register(ChatInfo)
