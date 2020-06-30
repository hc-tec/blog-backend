from django.urls import path
from . import views

urlpatterns = [
    # 用户注册
    path('register', views.RegisterUser.as_view()),
    # 获取单个用户信息
    path('userInfo', views.UserInfo.as_view()),
    # 获取所有用户的信息
    path('usersInfo', views.ShowAllUserInfo.as_view()),
    # 用户信息修改
    path('UserInfoModify/<int:pk>', views.UserInfoModify.as_view()),
    # 获取用户简单信息，用于聊天网页
    path('usersBriefInfo', views.ShowAllUserBriefInfo.as_view()),
    # 编写文章
    path('writeArticle', views.WriteArticle.as_view()),
    # 展示所有文章
    path('articles', views.ShowArticle.as_view()),
    # 某个用户的所有文章
    path('createdArticle/<int:pk>', views.SingleUserCreatedArticle.as_view()),
    # 文章归档
    path('articleFile', views.ShowArticleFile.as_view()),
    # 展示相应 id 的文章
    path('article', views.ShowSingleArticle.as_view()),
    # 博文置顶
    path('sticky/<int:pk>', views.StickyArticle.as_view()),
    # 更新博文点击数量
    path('clickNum', views.ArticleClickNumUpdate.as_view()),
    # 根据类别展示文章
    path('categoryArticle', views.GetArticleByCategory.as_view()),
    # 根据标签展示文章
    path('tagArticle', views.GetArticleByTag.as_view()),
    # 展示最近修改的文章
    path('updateArticle', views.ModifyArticle.as_view()),
    # 编辑相应的文章
    path('editArticle', views.EditArticle.as_view()),
    # 删除文章
    path('delArticle', views.DeleteArticle.as_view()),
    # 获取所有文章标签
    path('tags', views.ShowTag.as_view()),
    # 随机获取文章，用于推荐
    path('recommendArticle', views.RecommendArticle.as_view()),
    # 获取所有文章类别
    path('category', views.ShowCategory.as_view()),
    # 添加新的文章标签
    path('newTag', views.AddTag.as_view()),
    # 添加新的文章类别
    path('newCategory', views.AddCategory.as_view()),
    # 文件上传
    path('fileLoader', views.FileLoader.as_view()),
    # 获取 /static/ 文件夹中所有图片
    path('files', views.File.as_view()),
    # 用户登录
    path('login', views.UserLogin.as_view()),
    # 自动登录
    path('autoLogin', views.AutoLogin.as_view()),
    # 给相应 id 的用户添加新的任务
    path('newTask', views.AddTask.as_view()),
    # 获取相应 id 用户的任务清单
    path('task', views.ShowSingleTask.as_view()),
    # 获取所有任务清单
    path('tasks', views.ShowTask.as_view()),
    # 完成任务
    path('finishTask', views.finishTask.as_view()),
    # 获取完成的任务
    path('showFinishTask', views.ShowFinishTask.as_view()),
    # 获取所有任务标签
    path('showTaskTag', views.ShowTaskTag.as_view()),
    # 添加新的任务标签
    path('newTaskTag', views.AddTaskTag.as_view()),
    # 订阅博文
    path('subscribe', views.AddSubscribe.as_view()),
    # 展示博文评论
    path('showArticleComment/<int:pk>', views.ShowArticleComment.as_view()),
    # 添加博文评论
    path('addComment', views.AddArticleComment.as_view()),
    # 设置背景图片
    path('setBgImage/<int:pk>', views.SetBgImage.as_view()),
    # 根据用户创作数量进行排序
    path('rankList', views.UserListByArticleNum.as_view()),
]

