from users.models import User, Blog, Tag, Category, Task, TaskTag, FinishTask, BlogComment
from rest_framework import serializers
from django.core.serializers import serialize
import json
from datetime import datetime

class UserInfoSerializer(serializers.ModelSerializer):
    # chioces 展示
    gender = serializers.CharField(source='get_gender_display')
    user_type = serializers.CharField(source='get_user_type_display')
    regis_time = serializers.SerializerMethodField()
    login_time = serializers.SerializerMethodField()
    def get_login_time(self, row):
        if row.login_time:
            return datetime.strftime(row.login_time, '%Y-%m-%d %H:%M:%S')
        else:
            return datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    def get_regis_time(self, row):
        return datetime.strftime(row.regis_time, '%Y-%m-%d %H:%M:%S')
    class Meta:
        model = User
        fields = [
            'id', 'user_name', 'gender',
            'user_type', 'qq', 'regis_time',
            'login_time', 'avatar', 'hobby',
            'github', 'profile', 'isSubscribe', 'bgImage']

class UserBriefInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'user_name',  'avatar',]

class TaskTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskTag
        fields = '__all__'

def ListSerializer(instance):
    ser = json.loads(serialize('json', instance), encoding='utf-8')
    ret_list = []
    for ele in ser:
        name = ele['fields']['name']
        try:
            len_ = len(Blog.objects.filter(tag=Tag.objects.get(name=name)))
        except Exception:
            len_ = len(Blog.objects.filter(category=Category.objects.get(name=name)))
        ret_list.append({'name':name, 'num': len_})
    return ret_list


def FileSerializer(host, instance):
    ser = json.loads(serialize('json', instance), encoding='utf-8')
    return [f"http://{host}/static/{ele['fields']['name']}" for ele in ser]

class ArticleSerializer(serializers.ModelSerializer):
    # ForeignKey 类型自定义显示
    creator = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name')
    # ManyToMany 类型自定义显示
    tags = serializers.SerializerMethodField()
    contributor = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    modify_time = serializers.SerializerMethodField()
    avatar = serializers.CharField(source='creator.avatar')
    comment_num = serializers.SerializerMethodField()
    def get_comment_num(self, row):
        return len(row.comment_num.all())
    def get_creator(self, row):
        return {'id': row.creator.id, 'user_name': row.creator.user_name}
    def get_modify_time(self, row):
        return datetime.strftime(row.modify_time, '%Y-%m-%d %H:%M:%S')
    def get_create_time(self, row):
        return datetime.strftime(row.create_time, '%Y-%m-%d %H:%M:%S')
    def get_tags(self, row):
        return [tag.name for tag in row.tag.all()]
    def get_contributor(self, row):
        return [contributor.name for contributor in row.contributor.all()]
    class Meta:
        model = Blog
        fields = [
                    'id', 'title', 'content', 'create_time',
                    'modify_time', 'click_num', 'creator', 'avatar',
                    'category', 'contributor', 'tags', 'comment_num', 'weight']
        depth = 1


class ArticleFileSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_tag(self, row):
        return [tag.name for tag in row.tag.all()]

    def get_create_time(self, row):
        return datetime.strftime(row.create_time, '%Y-%m-%d')
    def get_creator(self, row):
        return {'id': row.creator.id, 'user_name': row.creator.user_name}
    class Meta:
        model = Blog
        depth = 1
        fields = ['id', 'title', 'creator', 'create_time', 'tag']

class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    tags = serializers.SerializerMethodField()
    def get_tags(self, row):
        return [tag.name for tag in row.tag.all()]
    class Meta:
        model = Task
        fields = ['id', 'user_id', 'task_name', 'startDay', 'endDay', 'interval', 'tags']
        depth = 1

class FinishTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    tags = serializers.SerializerMethodField()
    def get_tags(self, row):
        return [tag.name for tag in row.tag.all()]
    class Meta:
        model = FinishTask
        fields = ['task_name', 'startDay', 'endDay', 'finishDay', 'user_id', 'tags', 'advance', 'interval']
        depth = 1

class ArticleCommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    def get_create_time(self, row):
        return datetime.strftime(row.create_time, '%Y-%m-%d %H:%M:%S')
    def get_user(self, row):
        return {'name':row.user.user_name, 'avatar': row.user.avatar}
    def get_reply(self, row):
        reply = row.reply.all()
        ser = ArticleReplySerializer(instance=reply, many=True)
        return ser.data
    class Meta:
        model = BlogComment
        fields = ['id', 'user', 'message', 'create_time', 'reply']
        depth = 1

class ArticleReplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    def get_create_time(self, row):
        return datetime.strftime(row.create_time, '%Y-%m-%d %H:%M:%S')
    def get_user(self, row):
        return {'name': row.user.user_name, 'avatar': row.user.avatar}
    class Meta:
        model = BlogComment
        fields = ['id','user', 'message', 'create_time']
