from django.shortcuts import render_to_response,render

from django.http import HttpResponseRedirect,HttpResponse
from .models import Article,Comment,MyFavorite

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

import time
from datetime import datetime

# Create your views here.
def test(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return render_to_response("test.html",{'form':form})
    else:
        form = AuthenticationForm()
    return render_to_response("test.html", {
        'form': form,
    })


# 默认按照最新时间排序
def home(request):
    articles = Article.objects.all().order_by("-create_time")
    comments = Comment.objects.all()

    # comments = Comment.objects.all()
    article_info = []
    username = request.session.get('user', '')

    for article in articles:
        article_comments = [{'comment': comment.comment, 'author': comment.author.username, 'time': comment.create_time}
                            for comment in comments if comment.article.title == article.title]
        data = {}
        data['article'] = article
        data['article_comments'] = article_comments
        data['comments_num'] = len(article_comments)
        article_info.append(data)

    return render(request, 'home.html', {'article_info': article_info, 'user': username})


# 按照评论数进行排序
def popular(request):
    articles = Article.objects.all()
    comments = Comment.objects.all()

    # comments = Comment.objects.all()
    article_info = []
    username = request.session.get('user','')

    for article in articles:
        article_comments = [{'comment':comment.comment,'author':comment.author.username,'time':comment.create_time}
                            for comment in comments if comment.article.title == article.title]
        data = {}
        data['article'] = article
        data['article_comments'] = article_comments
        data['comments_num'] = len(article_comments)
        article_info.append(data)

    return render(request,'popular.html',{'article_info':reversed(sorted(article_info,
                                                                         key=lambda comment:comment['comments_num'])),
                                          'user':username})


# 创建新文章
@login_required
def create(request):
    """
    创建新文章
    """
    if request.method == 'POST':
        author_name = request.session.get('user','')
        title = request.POST.get('title','')
        tags = request.POST.get('tags','')
        content = request.POST.get('newcontent','')

        # 检查输入内容是否齐全
        if author_name and title and tags and content:
            # 检查文章标题是否重复
            if not Article.objects.filter(title=title):
                user = User.objects.get(username=author_name)
                now = datetime.fromtimestamp(time.time())
                new_article = Article.objects.create(author=user,title=title.lower(),tag=tags.lower(),content = content,create_time=now)
                new_article.save()

                return HttpResponseRedirect('/')
            message = 'Please change the title, it has been used'
            return HttpResponse(message)

        return HttpResponseRedirect('/')


# 添加评论
@login_required
def add_comment(request):

    if request.method == 'POST':
        author_name = request.session.get('user','')
        article_title = request.POST.get('article_title','')
        content = request.POST.get('comment_content','')

        if not author_name:
            return HttpResponseRedirect('/api/sign/')

        # if not follow_content

        if article_title and content:
            author = User.objects.get(username=author_name)
            article = Article.objects.get(title=article_title.lower())
            create_time = datetime.fromtimestamp(time.time())
            comment = Comment.objects.create(author=author, article=article, comment=content, create_time=create_time)
            comment.save()

            return HttpResponseRedirect('/')
        return HttpResponse('wrong'+'title'+str(article_title)+str(content))




# 用户信息
def userprofiles(request):
    return render(request, 'userprofiles.html')
