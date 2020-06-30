from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:chat_id>', views.chat),
    # 展示聊天内容
    path('chatInfo/<str:chat_id>', views.ShowChatInfo.as_view()),
]
