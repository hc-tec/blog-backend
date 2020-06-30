import os
from datetime import datetime, timedelta

from .models import (User, Blog, Category, Tag, Task, TaskTag, UserToken,
                     FinishTask, Files, Subscribe, BlogComment, ReplyComment)
from rest_framework.views import APIView
from rest_framework.viewsets import generics
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from .utils.pagination import SortedBlogPagination

from .utils.serializer import (UserInfoSerializer, ArticleSerializer, ListSerializer, TaskSerializer,
                            FinishTaskSerializer, FileSerializer, TaskTagSerializer, ArticleCommentSerializer,
                            ArticleFileSerializer, UserBriefInfoSerializer)
from .utils.function import (isUnique, orderDictToDict, isUniqueInTag, generateUUID, md5, getNowTimeString,
                            getIntervalOfTwoStrTime, getFiles, getDirname, updateArticleFormat, emailMatch, sendEmail)



class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 270, 'msg': '登录成功'}
        try:
            params, valid = orderDictToDict(request.data, False)
            obj = User.objects.filter(user_name=params['user_name'], password=params['password']).first()
            if obj:
                # 获取此用户的文章发布数量
                blog_num = len(Blog.objects.filter(creator=obj))
                # 创建或更新 Token
                user_token = UserToken.objects.filter(user=obj).first()
                if not user_token:
                    token = md5(params['user_name'])
                    UserToken.objects.update_or_create(user=obj, defaults={'token': token})
                else:
                    user_token = user_token.__dict__['token']
                    token = user_token

                # 最近登录的时间
                u = User.objects.get(user_name=params['user_name'])
                u.login_time = datetime.now()
                u.save()

                ret['token'] = token
                ser = UserInfoSerializer(instance=obj, many=False)
                ret['data'] = ser.data
                ret['data']['article_num'] = blog_num
            else:
                ret['code'] = 470
                ret['msg'] = '该用户信息不存在喔'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class AutoLogin(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 270, 'msg': '自动登录'}
        try:
            token = request.data['token']
            # 一对一关系模型数据获取
            user_name = UserToken.objects.get(token=token).user
            obj = User.objects.filter(user_name=user_name)
            if obj:
                # 获取此用户的文章发布数量
                blog_num = len(Blog.objects.filter(creator=obj.first()))
                # 最近登录的时间
                u = User.objects.get(user_name=user_name)
                u.login_time = datetime.now()
                u.save()

                ser = UserInfoSerializer(instance=obj, many=True)
                ret['data'] = ser.data
                ret['data'][0]['article_num'] = blog_num
            else:
                ret['code'] = 470
                ret['msg'] = '自动登录失败'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 271, 'msg': '注册成功，新添一员大将'}
        try:
            params, flag = orderDictToDict(request.data, True, ["friend_card", 'hobby', 'github', 'profile'])
            repeat = isUnique(params['user_name'], User)[0]
            if repeat:
                ret['code'] = 720
                ret['msg'] = "用户名重复了喔，重选一个吧"
            if not repeat and flag:
                User.objects.create(**params)
            elif not flag:
                ret['code'] = 710
                ret['msg'] = "信息还是完整点的好康吧"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class UserInfo(APIView):
    def get(self, request, *args, **kwargs):
        ret = {"code": 272, "msg": "用户信息查询成功"}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist, info = isUnique(params['user_name'], User)
                if exist:
                    ser = UserInfoSerializer(instance=info, many=True)
                    ret['data'] = ser.data
                else:
                    ret['code'] = 810
                    ret['msg'] = "欧欧，不存在该用户哦，要不注册一个吧"
            else:
                ret['code'] = 820
                ret['msg'] = "谁，又甘愿做，，，无名之辈呢"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowAllUserInfo(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 286, 'msg': '获取所有用户信息成功'}
        try:
            info = User.objects.all()
            ser = UserInfoSerializer(instance=info, many=True)
            ret['data'] = ser.data
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowAllUserBriefInfo(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserBriefInfoSerializer


class UserInfoModify(APIView):
    def patch(self, request, *args, **kwargs):
        ret = {'code': 289, 'msg': '修改成功'}
        data, _ = orderDictToDict(request.data, False)
        User_obj = User.objects.filter(pk=kwargs['pk'])
        if User_obj:
            User_obj.update(**data)
        else:
            ret['code'] = 810
            ret['msg'] = '用户不存在'
        return JsonResponse(ret)


class WriteArticle(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 273, 'msg': '又是佳作一篇，继续坚持！！！'}
        try:
            params, valid = orderDictToDict(request.data, False)
            if valid:
                # 给 Blog.creator 传 User (instance对象)
                creator = User.objects.filter(user_name=params['creator']).first()
                if not creator:
                    ret['code'] = 940
                    ret['msg'] = "该创作者不存在yo，注册一个吧"
                    return JsonResponse(ret)
                # 给 Blog.category 传 Category (instance对象)
                category = Category.objects.filter(name=params['category']).first()
                if not category:
                    ret['code'] = 950
                    ret['msg'] = "该类别不存在yo，新建一个吧"
                    return JsonResponse(ret)
                params['creator'] = creator
                params['category'] = category
                # 给 Blog.tag 添加 Tag (instance对象)
                tags = [Tag.objects.filter(name=tag).first() for tag in params['tag'].split(',')]
                del params['tag']
                # 对 js 传来的 encodeURIComponent 编码数据进行解析
                blog = Blog.objects.create(**params)
                for tag in tags:
                    blog.tag.add(tag)
                # 博文 id
                id = Blog.objects.filter(title=params['title'], creator=params['creator']).first().__dict__['id']
                # 订阅者邮件
                receive_list = [info[1] for info in Subscribe.objects.values_list()]
                # sendEmail(receive_list, params, id)
            else:
                ret['code'] = 910
                ret['msg'] = "残缺的博文不完美喔"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowArticle(generics.ListAPIView):
    pagination_class = SortedBlogPagination
    queryset = Blog.objects.all().order_by("-weight", "-create_time")
    serializer_class = ArticleSerializer


class ShowArticleFile(generics.ListAPIView):
    queryset = Blog.objects.all().order_by("create_time")
    serializer_class = ArticleFileSerializer


class ShowSingleArticle(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 279, 'msg': '博文获取成功'}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist = Blog.objects.filter(id=params['id']).first()
                if exist:
                    # 文章数据序列化
                    ser = ArticleSerializer(instance=exist, many=False)
                    ret['data'] = ser.data
                else:
                    ret['code'] = 950
                    ret['msg'] = "木有你指定的文章喔"
            else:
                ret['code'] = 960
                ret['msg'] = '我也希望这世上存在会隐形的参数。。。'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class SingleUserCreatedArticle(generics.ListAPIView):
    serializer_class = ArticleFileSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return Blog.objects.filter(creator=User.objects.filter(pk=id).first()).order_by('-create_time')


class RecommendArticle(generics.ListAPIView):
    serializer_class = ArticleFileSerializer
    def get_queryset(self):
        return Blog.objects.order_by('?')[:5]


class StickyArticle(APIView):
    def patch(self, request, *args, **kwargs):
        ret = {'code': 287, 'msg': '置顶成功'}
        try:
            Blog_obj = Blog.objects.get(pk=kwargs['pk'])
            if Blog_obj:
                Blog_obj.__dict__['weight'] = 2020
                Blog_obj.save()
            else:
                ret['code'] = 950
                ret['msg'] = '博文不存在'
        except Exception as e:
            print(e)
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {'code': 288, 'msg': '取消置顶成功'}
        try:
            Blog_obj = Blog.objects.get(pk=kwargs['pk'])
            if Blog_obj:
                Blog_obj.__dict__['weight'] = 0
                Blog_obj.save()
            else:
                ret['code'] = 950
                ret['msg'] = '博文不存在'
        except Exception as e:
            print(e)
        return JsonResponse(ret)


class EditArticle(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 283, 'msg': '编辑博文成功'}
        try:
            params, valid = orderDictToDict(request.data, False)
            if valid:
                blog = Blog.objects.filter(pk=params['id'])
                if not blog:
                    ret['code'] = 940
                    ret['msg'] = "该博文不存在yo，创建一个吧"
                    return JsonResponse(ret)
                # 给 Blog.creator 传 User (instance对象)
                creator = User.objects.filter(user_name=params['creator']).first()
                if not creator:
                    ret['code'] = 940
                    ret['msg'] = "该创作者不存在yo，注册一个吧"
                    return JsonResponse(ret)
                # 给 Blog.category 传 Category (instance对象)
                category = Category.objects.filter(name=params['category']).first()
                if not category:
                    ret['code'] = 950
                    ret['msg'] = "该类别不存在yo，新建一个吧"
                    return JsonResponse(ret)
                params['creator'] = creator
                params['category'] = category
                params['modify_time'] = datetime.now()
                # 给 Blog.tag 添加 Tag (instance对象)
                tags = [Tag.objects.filter(name=tag).first() for tag in params['tag'].split(',')]
                del params['tag']
                # 更新博文
                blog.update(**params)
                # 更新标签
                blog.first().tag.clear()
                blog.first().tag.add(*tags)
            else:
                ret['code'] = 910
                ret['msg'] = "残缺的博文不完美喔"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ModifyArticle(APIView):
    def get(self, request, *args, **kwargs):
        ret = {}
        # 筛选出最近的创建时间与修改时间不相等的文章
        latest_day = 15
        max_articles = 5
        blog = [updateArticleFormat(article) for article in Blog.objects.all().order_by('-modify_time').values() if 1000 < getIntervalOfTwoStrTime(article['create_time'],article['modify_time'], 'microseconds') and latest_day > getIntervalOfTwoStrTime(datetime.now(), article['modify_time'])][:max_articles]
        ret['data'] = blog
        return JsonResponse(ret)


class DeleteArticle(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 281, 'msg': '博文删除成功'}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist = Blog.objects.filter(id=params['id'])
                if exist:
                    exist.delete()
                else:
                    ret['code'] = 950
                    ret['msg'] = "木有你指定的文章喔"
            else:
                ret['code'] = 951
                ret['msg'] = '我也希望这世上存在会隐形的参数。。。'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class AddTag(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 275, 'msg': '标签，让文章新增乐趣'}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist = isUniqueInTag(params['name'], Tag)[0]
                if exist:
                    ret['code'] = 930
                    ret['msg'] = "%s ：“呜呜呜，你竟然看不见我”" % params['name']
                else:
                    Tag.objects.create(**params)
            else:
                ret['code'] = 940
                ret['msg'] = '无字,,,标签？'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class AddCategory(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 276, 'msg': '类，让文章条理清晰'}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist = isUniqueInTag(params['name'], Category)[0]
                if exist:
                    ret['code'] = 950
                    ret['msg'] = "%s ：“呜呜呜，你竟然看不见我”" % params['name']
                else:
                    Category.objects.create(**params)
            else:
                ret['code'] = 960
                ret['msg'] = '无字,,,类别？'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowTag(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'code': 277,
            'msg': '所有标签都在这了，拿去吧'
        }
        try:
            tags = Tag.objects.all().order_by("name")
            if tags:
                tagsList = ListSerializer(tags)
                ret['data'] = tagsList
            else:
                ret['code'] = 921
                ret['msg'] = "暂无任何标签噢，赶紧去添加几个 bia~~"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowCategory(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'code': 278,
            'msg': '所有类别都在这了，拿去吧'
        }
        try:
            category = Category.objects.all()
            if category:
                ser = ListSerializer(category)
                ret['data'] = ser
            else:
                ret['code'] = 922
                ret['msg'] = "暂无任何类别噢，赶紧去添加几个 bia~~"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class File(APIView):
    file_dir = getDirname() + '/static/'
    files = getFiles(file_dir)

    def get(self, request, *args, **kwargs):
        ret = {'code': 284, 'msg': '获取图像文件成功'}
        try:
            host = request.get_host()
            files = Files.objects.all()
            img_files = FileSerializer(host,files)
            if img_files:
                ret['data'] = img_files
            else:
                ret['code'] = 1100
                ret['msg'] = '文件内无任何文件'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {'code': 285, 'msg': '图像删除成功'}
        try:
            file_name = request._request.GET.get('file_name')
            files = Files.objects.filter(name=file_name)
            if files:
                files.delete()
            if file_name in self.files:
                os.remove(f'{self.file_dir}{file_name}')
            else:
                ret['code'] = 1110
                ret['msg'] = '改文件不存在喔'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class FileLoader(APIView):
    def post(self, request, *args, **kwargs):
        ret = {}
        img_type = ['png', 'gif', 'jpeg', 'bmp', 'jpg', 'tif', 'svg', 'webp']
        try:
            file = request.FILES.get('file')
            if file:
                file.name = file.name.replace('\"', '') or file.name
                file_type = (file.name).split('.')[1] or None
                if file_type and file_type in img_type:
                    file.name = generateUUID(file.name)
                    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    destination = open(os.path.join(BASE_DIR, 'static/' + file.name), 'wb+')
                    for chunk in file.chunks():
                        destination.write(chunk)
                    destination.close()
                    host = request.get_host()
                    Files.objects.create(name=file.name)
                    ret = {'code': 282, 'msg': f'http://{host}/static/{file.name}'}
                else:
                    ret['code'] = 953
                    ret['msg'] = '不支持改类型文件'
            else:
                ret['code'] = 952
                ret['msg'] = '文件为空，上传失败啦'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowTaskTag(generics.ListAPIView):
    queryset = TaskTag.objects.all()
    serializer_class = TaskTagSerializer


class AddTaskTag(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 296, 'msg': '添加任务标签成功'}
        try:
            params, valid = orderDictToDict(request._request.GET, True)
            if valid:
                exist = isUniqueInTag(params['name'], TaskTag)[0]
                if exist:
                    ret['code'] = 930
                    ret['msg'] = "%s ：“呜呜呜，你竟然看不见我”" % params['name']
                else:
                    TaskTag.objects.create(**params)
            else:
                ret['code'] = 940
                ret['msg'] = '无字,,,标签？'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class AddTask(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 290, 'msg': '任务添加成功'}
        try:
            params, valid = orderDictToDict(request._request.GET, False)
            if valid:
                user = User.objects.filter(pk=params['user']).first()
                if user:
                    params['user'] = user
                    tags = [TaskTag.objects.filter(name=tag).first() for tag in params['tag'].split(',')]
                    del params['tag']
                    interval = getIntervalOfTwoStrTime(params['startDay'], params['endDay'])
                    params['interval'] = interval
                    # 对 js 传来的 encodeURIComponent 编码数据进行解析
                    task = Task.objects.create(**params)
                    for tag in tags:
                        task.tag.add(tag)
                else:
                    ret['code'] = 610
                    ret['msg'] = '还少了点什么呢？'
            else:
                ret['code'] = 610
                ret['msg'] = '还少了点什么呢？'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class finishTask(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 291, 'msg': '任务完成了，棒棒哒！'}
        try:
            id = request._request.GET.get('id')
            if id:
                task = Task.objects.filter(pk=id).first()
                if task:
                    task.delete()
                    task = task.__dict__
                    del task['_state']
                    del task['id']
                    advance = getIntervalOfTwoStrTime(task['startDay'], task['endDay'])
                    task['advance'] = advance
                    task['finishDay'] = getNowTimeString()
                    FinishTask.objects.create(**task)
                else:
                    ret['code'] = 610
                    ret['msg'] = '参数为空或者该任务已经被删除了喔，删除任务失败'
            else:
                ret['code'] = 610
                ret['msg'] = '参数为空或者该任务已经被删除了喔，删除任务失败'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowFinishTask(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 294, 'msg': '不仅是任务，是坚持!更是成就!'}
        try:
            params, valid = orderDictToDict(request._request.GET, False)
            if valid:
                user = User.objects.get(pk=params['id'])
                task = user.finishtask_set.all()
                ser = FinishTaskSerializer(instance=task, many=True)
                ret['data'] = ser.data
            else:
                ret['code'] = 610
                ret['msg'] = '我也希望这世上存在会隐形的参数'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowTask(APIView):
    def post(self, request, *args, **kwargs):
        ret = {
            'code': 295,
            'msg': '所有任务都在这了，拿去吧'
        }
        try:
            tasks = Task.objects.all()
            if tasks:
                ser = TaskSerializer(instance=tasks, many=True)
                ret['data'] = ser.data
            else:
                ret['code'] = 920
                ret['msg'] = "暂无任何任务噢，赶紧添加些吧"
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowSingleTask(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 292, 'msg': '任务获取成功了，也要努力去执行喔'}
        try:
            params, valid = orderDictToDict(request._request.GET, False)
            if valid:
                user = User.objects.get(pk=params['id'])
                task = user.task_set.all()
                ser = TaskSerializer(instance=task, many=True)
                # 获取剩余天数
                for task in ser.data:
                    task['leftDay'] = getIntervalOfTwoStrTime(getNowTimeString(), task['endDay'])
                ret['data'] = ser.data
            else:
                ret['code'] = 610
                ret['msg'] = '我也希望这世上存在会隐形的参数'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class GetArticleByCategory(APIView):

    def get(self, request, *args, **kwargs):
        ret = {'code': 297, 'msg': '就是这些了'}

        category = request._request.GET.get('name') or None
        category_obj = Category.objects.filter(name=category).first() or None
        article_obj = Blog.objects.filter(category=category_obj).order_by("-create_time") or None
        ret['data'] = ArticleSerializer(instance=article_obj, many=True).data

        return JsonResponse(ret)


class GetArticleByTag(APIView):

    def get(self, request, *args, **kwargs):
        ret = {'code': 298, 'msg': '就是这些了'}

        tag = request._request.GET.get('name') or None
        tag_obj = Tag.objects.filter(name=tag).first() or None
        article_obj = Blog.objects.filter(tag=tag_obj).order_by("-create_time") or None
        ret['data'] = ArticleSerializer(instance=article_obj, many=True).data

        return JsonResponse(ret)


class AddSubscribe(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code':299, 'msg':'订阅成功'}
        try:
            email = request._request.GET.get('email', '')
            if emailMatch(email):
                obj = Subscribe.objects.filter(email=email).first()
                if not obj:
                    Subscribe.objects.create(email=email)
                    user = User.objects.filter(qq=email.split('@')[0]).first()
                    if user:
                        user.isSubscribe = True
                        user.save()
                else:
                    ret['code'] = 1201
                    ret['msg'] = '您已订阅了喔'
            else:
                ret['code'] = 1100
                ret['msg'] = '邮箱格式错误!'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {'code': 241, 'msg': '取消订阅成功'}
        try:
            email = request._request.GET.get('email', '')
            if emailMatch(email):
                try:
                    print(1)
                    Subscribe.objects.filter(email=email).first().delete()
                    print(1)
                    user = User.objects.filter(qq=email.split('@')[0]).first()
                    if user:
                        print(2)
                        user.isSubscribe = False
                        user.save()
                except Exception as e:
                    print(e)
                    ret['code'] = 1200
                    ret['msg'] = '此邮箱未订阅文章喔'
            else:
                ret['code'] = 1100
                ret['msg'] = '邮箱格式错误!'
        except Exception as e:
            ret = {'code': 1000, 'msg': '未知错误'}
            print(e)
        return JsonResponse(ret)


class ShowArticleComment(generics.ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleCommentSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return BlogComment.objects.filter(blog=Blog.objects.filter(pk=id).first()).order_by("-create_time")


class AddArticleComment(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code':1200}
        params, valid = orderDictToDict(request._request.GET, True)
        if valid:
            user = User.objects.filter(pk=params['user']).first()
            blog = Blog.objects.filter(pk=params['blog']).first()
            if user and blog:
                params['user'] = user
                params['blog'] = blog
                BlogComment.objects.create(**params)
            else:
                ret = {'code': 1301, 'msg': '不存在用户或博文未知'}
        else:
            ret = {'code': 1300, 'msg':'参数不足'}
        return JsonResponse(ret)

    def post(self, request, *args, **kwargs):
        ret = {'code': 1200}
        params, valid = orderDictToDict(request.data, True)
        if valid:
            user = User.objects.filter(pk=params['user']).first()
            replied_comment = BlogComment.objects.filter(pk=params['replied_comment']).first()
            if user:
                params['user'] = user
                params['replied_comment'] = replied_comment
                ReplyComment.objects.create(**params)
            else:
                ret = {'code': 1301, 'msg': '不存在用户或博文未知'}
        else:
            ret = {'code': 1300, 'msg': '参数不足'}
        return JsonResponse(ret)


class ArticleClickNumUpdate(APIView):
    def get(self, request, *args, **kwargs):
        id = request._request.GET.get('id')
        article = Blog.objects.filter(pk=id)
        click_num = article[0].__dict__['click_num']
        click_num += 1
        article.update(click_num=click_num)

        return JsonResponse({})


class SetBgImage(APIView):
    def get(self, request, *args, **kwargs):
        ret = {'code': 242, 'msg': '背景图片设置成功'}
        try:
            image = request._request.GET.get('image')
            User_obj = User.objects.get(pk=kwargs['pk'])
            if User_obj:
                User_obj.__dict__['bgImage'] = image
                User_obj.save()
            else:
                ret['code'] = 810
                ret['msg'] = '此用户不存在'
        except Exception as e:
            print(e)
        return JsonResponse(ret)


class UserListByArticleNum(APIView):
    def get(self, request, *args, **kwargs):
        Users = User.objects.all()
        def rank():
            ranklist = []
            for User_ in Users:
                try:
                    start = datetime.today() - timedelta(days=30)
                    num = len(Blog.objects.filter(create_time__gt=(start), creator=User_))
                except Exception:
                    num = 0
                ranklist.append({
                    'id': User_.__dict__['id'],
                    'user_name': User_.__dict__['user_name'],
                    'len': num
                })
            ranklist.sort(key=lambda x:x['len'], reverse=True)
            return ranklist[:5]
        return JsonResponse({
            'data': rank()
        })

