from django.db import models

class User(models.Model):

    USER_TYPE = (
        (1, '普通用户'),
        (2, '管理员'),
        (3, '超级管理员')
    )
    GENDER = (
        ('male', '男'),
        ('female', '女')
    )
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=8,choices=GENDER, default='male')
    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    avatar = models.CharField(max_length=128, null=True,blank=True)
    qq = models.CharField(max_length=16)
    friend_card = models.CharField(max_length=10, null=True,blank=True)
    regis_time = models.DateTimeField(auto_now_add=True)
    login_time = models.DateTimeField(default=None, null=True)
    hobby = models.CharField(max_length=256, null=True,blank=True)
    github = models.CharField(max_length=128, null=True,blank=True)
    profile = models.CharField(max_length=1024, null=True,blank=True)
    isSubscribe = models.BooleanField(null=True, default=False)
    bgImage = models.CharField(max_length=128, default='' ,null=True, blank=True)

    def __str__(self):
        return self.user_name

class UserToken(models.Model):
    user = models.OneToOneField(to='User', on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=64)

class Blog(models.Model):

    title = models.CharField(max_length=32)
    content = models.TextField(default='')
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    contributor = models.ManyToManyField("User", default=None, related_name='+')
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)
    click_num = models.IntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag", default=None)
    weight = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.title

class BaseComment(models.Model):

    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.create_time}"

class BlogComment(BaseComment):
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE, related_name="comment_num")

class ReplyComment(BaseComment):
    replied_comment = models.ForeignKey("BlogComment",
                                        on_delete=models.CASCADE,
                                        null=True, blank=True,
                                        related_name="reply")

class Category(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return self.name

class Word(models.Model):

    word = models.CharField(max_length=32)
    hans = models.CharField(max_length=128)
    creator = models.OneToOneField(to="User", on_delete=models.CASCADE)
    contributor = models.ManyToManyField("User", related_name='+')
    relevant = models.ManyToManyField("Relevant", related_name='+')
    public_user = models.ManyToManyField("User", related_name='+')

    def __str__(self):
        return self.word

class Phrase(models.Model):
    word = models.ForeignKey("Word", on_delete=models.CASCADE, related_name='+')
    phrase_eng = models.CharField(max_length=64)
    phrase_hans = models.CharField(max_length=64)

    def __str__(self):
        return self.phrase_eng

class Sentence(models.Model):
    word = models.ForeignKey("Word", on_delete=models.CASCADE, related_name='+')
    sentence_eng = models.CharField(max_length=256)
    sentence_hans = models.CharField(max_length=256)

    def __str__(self):
        return self.sentence_eng

class Relevant(models.Model):

    word = models.CharField(max_length=32)

    def __str__(self):
        return self.word

class Task(models.Model):

    task_name = models.CharField(max_length=64)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    tag = models.ManyToManyField("TaskTag")
    startDay = models.CharField(max_length=32)
    endDay = models.CharField(max_length=32)
    interval = models.IntegerField(default=3)

    def __str__(self):
        return self.task_name

class FinishTask(models.Model):

    task_name = models.CharField(max_length=64)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    tag = models.ManyToManyField("TaskTag")
    startDay = models.CharField(max_length=32)
    endDay = models.CharField(max_length=32)
    finishDay = models.CharField(max_length=32)
    interval = models.IntegerField(default=3)
    advance = models.IntegerField(default=0)

    def __str__(self):
        return self.task_name

class TaskTag(models.Model):

    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Files(models.Model):

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Subscribe(models.Model):

    email = models.CharField(max_length=128)

    def __str__(self):
        return self.email
