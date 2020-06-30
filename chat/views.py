import json
import datetime
import pickle

from dwebsocket.decorators import accept_websocket
# from rest_framework.views import APIView
# from django.http import JsonResponse
from rest_framework.viewsets import generics
from rest_framework.pagination import PageNumberPagination


from .models import (ChatInfo, ChatRoom)
from .utils.serializer import (ChatInfoSerializer,)

allUserChatSocket = {}
@accept_websocket
def chat(request, **kwargs):
    global allUserChatSocket
    try:
        if request.is_websocket():
            first, second = kwargs['chat_id'].split('-')
            user_id = first[1:] if 'u' in first else second[1:]
            if first != second:
                id = kwargs['chat_id'].replace('u', '')
                allUserChatSocket[id] = allUserChatSocket.get(id, {})
                allUserChatSocket[id][user_id] = request.websocket
                print(pickle.dumps(request.websocket))
                for message in request.websocket:
                    print(allUserChatSocket.values())
                    # message_save = json.loads(str(message, 'utf-8'), encoding='utf-8')
                    # addChatMessage(id, message_save)
                    for val in allUserChatSocket[id].values():
                        val.send(message)
    except Exception as e:
        print(e)
        print("一个 WebSocket 终止")


def addChatMessage(chat_room_id: str, message: dict) -> None:
    chat_room = ChatRoom.objects.filter(chat_id=chat_room_id).first()
    if not chat_room:
        chat_room = ChatRoom.objects.create(chat_id=chat_room_id)
    message['chat_room'] = chat_room
    message['user_id'] = message['id']
    del message['id']
    ChatInfo.objects.create(**message)

class ChatInfoPagination(PageNumberPagination):
    page_size = 10

class ShowChatInfo(generics.ListAPIView):
    serializer_class = ChatInfoSerializer
    pagination_class = ChatInfoPagination
    def get_queryset(self):
        first, second = self.kwargs['chat_id'].split('-')
        id = f'{first}-{second}'.replace('u', '')
        return ChatInfo.objects.filter(chat_room=id)






