from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect,HttpResponse, HttpRequest,Http404
from .models import Article,Comment,MyFavorite,MyLike
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
import time
from datetime import datetime

# Create your views here.
def test(request):
    request_data=[]
    for i in request.META:
        data={}
        data[i]=request.META[i]
        request_data.append(data)
    return render(request, 'test.html',{'request_data':request_data})



# 默认按照最新时间排序
def home(request):
    # 获取所有文章，评论，按文章创建时间倒序排列
    articles = Article.objects.all().order_by("-create_time")
    comments = Comment.objects.all()

    article_info = []
    user = request.user

    # 获取文章评论
    for article in articles:
        article_comments = article.comment_set.all()
        data = {}
        data['article'] = article
        data['article_comments'] = article_comments
        # data['comments_num'] = len(article_comments)
        article_info.append(data)

    # 如果用户登录，返回用户的收藏夹数据，否则不返回
    if user.username:
        favorite_collector = MyFavorite.objects.get(collector=user)
        collections = [article.title for article in favorite_collector.collection.all()]
        return render(request, 'home.html', {'article_info': article_info, 'collections':collections,})

    return render(request, 'home.html', {'article_info': article_info, })


# 按照评论数进行排序
def popular(request):
    articles = Article.objects.all()
    comments = Comment.objects.all()

    article_info = []
    user = request.user

    for article in articles:
        article_comments = article.comment_set.all()
        data = {}
        data['article'] = article
        data['article_comments'] = article_comments
        data['comments_num'] = len(article_comments)
        article_info.append(data)

    if user.username:
        favorites = MyFavorite.objects.get(collector=user)
        collections = [article.title for article in favorites.collection.all()]
        # 按评论数倒序排列，并添加用户收藏夹数据
        return render(request, 'popular.html', {'article_info':reversed(sorted(article_info,key=lambda comment:comment['comments_num'])), 'collections':collections})
    # 按评论数倒序排列
    return render(request,'popular.html',{'article_info':sorted(article_info,key=lambda comment:comment['comments_num'])})


# 用户信息
@login_required
def userprofiles(request):

    user = request.user

    articles = Article.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    myfavorites = MyFavorite.objects.get(collector=user)

    my_article = []
    my_favorite = []
    my_comment = []
    collections=[]


    if articles:

        for article in articles:
            article_comments = article.comment_set.all()
            data = {}
            data['article'] = article
            data['article_comments'] = article_comments
            data['comments_num'] = len(article_comments)
            my_article.append(data)


    if comments:
        for comment in comments:
            data = {}
            data['article'] = comment.article
            data['article_comments'] =comment.article.comment_set.all()
            data['comments_num'] = len(comment.article.comment_set.all())
            my_comment.append(data)


    if myfavorites:
        for article in myfavorites.collection.all():
            data={}
            data['article'] = article
            data['article_comments'] = article.comment_set.all()
            data['comments_num'] = len(article.comment_set.all())
            my_favorite.append(data)
            collections.append(article.title)

    return render(request, 'userprofiles.html', {'my_article': my_article, 'my_favorite':my_favorite,'my_comment':my_comment,'collections':collections})

        # return render(request, 'home.html', {'article_info': article_info, 'user': username})
