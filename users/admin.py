from django.contrib import admin
from .models import (User, Blog, Word, Phrase, Sentence, Relevant, Category,
                     Tag, Task, TaskTag, UserToken, FinishTask, Files, Subscribe, BlogComment, ReplyComment)
# Register your models here.

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Word)
admin.site.register(Phrase)
admin.site.register(Sentence)
admin.site.register(Relevant)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Task)
admin.site.register(FinishTask)
admin.site.register(TaskTag)
admin.site.register(UserToken)
admin.site.register(Files)
admin.site.register(Subscribe)
admin.site.register(BlogComment)
admin.site.register(ReplyComment)

