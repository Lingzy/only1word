from oneword.models import Article, Comment, MyFavorite
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist


# 返回文章列表接口
def allarticle(request):

    if request.method == 'GET':
        article_list = []
        all_article = Article.objects.all()
        for article in all_article:
            data = {}
            data['author'] = article.author.username
            data['title'] = article.title
            data['tag'] = article.tag
            article_list.append(data)

        return JsonResponse({'status': 200, 'article_list': article_list, 'message': 'success'})
    return JsonResponse({'status': 10023, 'message': 'Please use GET method'})


# 根据作者返回文章信息接口
def get_article_author(request):

    if request.method == 'GET':
        author = request.GET.get('author', '')

        if author == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        articles = Article.objects.filter(author__username=author.lower())
        article_list = []
        if articles:
            for article in articles:
                data = {}
                data['title'] = article.title
                data['tag'] = article.tag
                data['id'] = article.id
                article_list.append(data)
            return JsonResponse({'status': 200, 'data': article_list, 'author': author, 'message': 'success'})
        return JsonResponse({'status': 10022, 'message': 'No result'})



# 根据文章名称返回文章信息
def get_article_title(request):

    if request.method == 'GET':
        title = request.GET.get('title', '')

        if title == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        articles = Article.objects.filter(title__contains=title.lower())
        article_list = []
        if articles:
            for article in articles:
                data = {}
                data['title'] = article.title
                data['author'] = article.author.username
                data['tag'] = article.tag
                data['id'] = article.id
                article_list.append(data)
            return JsonResponse({'status': 200, 'data': article_list, 'message': 'success'})
        return JsonResponse({'status': 10022, 'message': 'No result'})


# 根据文章tag返回文章信息
def get_article_tag(request):

    if request.method == 'GET':
        tag = request.GET.get('tags', '')

        if tag == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        articles = Article.objects.filter(tag__contains=tag.lower())
        article_list = []
        if articles:
            for article in articles:
                data = {}
                data['title'] = article.title
                data['author'] = article.author.username
                data['tag'] = article.tag
                data['id'] = article.id
                article_list.append(data)
            return JsonResponse({'status': 200, 'data': article_list, 'message': 'success'})
        return JsonResponse({'status': 10022, 'message': 'No result'})


# 判断是否是自己的文章
@login_required
def my_own_article(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        user = request.user

        if id and user:
            article = Article.objects.get(id=id)
            if article.author == user:
                return JsonResponse({'status': 200, 'message': 'this is your own article'})
            else:
                return JsonResponse({'status': 10022, 'message': 'this is not your article'})
        else:
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

# 检查文章标题是否重复
def is_title_used(request):
    if request.method =='GET':
        title = request.GET.get('title','')
        try:
            article = Article.objects.get(title=title.lower())

            return JsonResponse({'status':200,'message':'Title exist'})
        except:
            return JsonResponse({'status':10021,'message':'Title not used'})



# 收藏文章接口
@login_required
def article_favorite(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id', '')
        user = request.user

        if not user:
            return JsonResponse({'status': 10021, 'message': 'Please sign in first'})

        if id == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        # 添加收藏
        article = Article.objects.get(id=id)
        myfavorite = MyFavorite.objects.get(collector=user)
        # 判断文章是否在收藏列表
        if article not in myfavorite.collection.all():
            myfavorite.collection.add(article)
            myfavorite.save()
            # 增加收藏数
            article.favorite += 1
            article.save()
            return JsonResponse({'status': 200, 'article_id': article.id, 'favorite': article.favorite, 'message': 'add to favorite success'})
        return JsonResponse({'status': 10024, 'message': 'you have collected this article'})

    return JsonResponse({'status': 10023, 'message': 'not GET method'})

# 取消收藏文章接口


@login_required
def article_unfavorite(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id', '')
        user = request.user

        if not user:
            return JsonResponse({'status': 10020, 'message': 'Please sign in first'})

        if id == '':
            return JsonResponse({'status': 10021, 'message': 'parameter error'})

        # 取消收藏
        article = Article.objects.get(id=id)

        # user = User.objects.get(username=username)
        myfavorite = MyFavorite.objects.get(collector=user)
        if article in myfavorite.collection.all():
            myfavorite.collection.remove(article)
            myfavorite.save()
            # 减少收藏数
            article.favorite -= 1
            article.save()
            return JsonResponse({'status': 200, 'article_id': article.id, 'favorite': article.favorite, 'message': 'add dislike success'})
        else:
            return JsonResponse({'status': 10022, 'message': 'You have not collect this article yet'})
    return JsonResponse({'status': 10023, 'message': 'not GET method'})


# 创建新文章
@login_required
def create(request):
    """
    创建新文章
    """
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title', '')
        tags = request.POST.get('tags', '')
        content = request.POST.get('content', '')

        # 检查用户是否登录
        if not user:
            return JsonResponse({'status': 10021, 'message': 'User not login'})

        # 检查数据是否完整
        if title and tags and content:
            # 检查文章标题是否重复
            if not Article.objects.get(title=title):
                now = datetime.fromtimestamp(time.time())
                new_article = Article.objects.create(author=user, title=title.lower(), tag=tags.lower(), content=content, create_time=now)
                new_article.save()
                return JsonResponse({'status': 200, 'message': 'Create article success'})
            else:
                return JsonResponse({'status': 10021, 'message': 'This title was has been used'})

        return JsonResponse({'status': 10022, 'message': 'Data not completed'})


# 添加评论
@login_required
def add_comment(request):

    if request.method == 'POST':
        user = request.user
        article_title = request.POST.get('article_title', '')
        content = request.POST.get('comment_content', '')

        # 判断是否登录
        if not user:
            return JsonResponse({'status': 10021, 'message': 'User not login'})

        # 判断数据是否完整
        if article_title and content:
            article = Article.objects.get(title=article_title.lower())
            create_time = datetime.fromtimestamp(time.time())
            comment = Comment.objects.create(
                author=user, article=article, comment=content, create_time=create_time)
            comment.save()
            return JsonResponse({'status': 200, 'message': 'Add comment success'})
        else:
            return JsonResponse({'status': 10022, 'message': 'Data not completed'})

# test api


def test_tab(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_data = []

        for user in users:
            data = {}
            data['username'] = user.username
            data['userid'] = user.id
            user_data.append(data)
        return JsonResponse({'status': 200, 'msg': 'success', 'data': user_data})
    return JsonResponse({'status': 10021, 'msg': 'API failed'})
