from django.db import models

class ChatRoom(models.Model):

    chat_id = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.chat_id

class ChatInfo(models.Model):

    chat_room = models.ForeignKey(to="ChatRoom", on_delete=models.CASCADE)
    user_id = models.IntegerField(default=0, null=True)
    user_name = models.CharField(max_length=20, default='')
    avatar = models.CharField(max_length=256, blank=True, null=True)
    message = models.TextField()
    send_time = models.CharField(max_length=32)


