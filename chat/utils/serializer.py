from ..models import (ChatRoom, ChatInfo)
from rest_framework import serializers

class ChatInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatInfo
        fields = ['id', 'user_name', 'avatar', 'message', 'send_time']
