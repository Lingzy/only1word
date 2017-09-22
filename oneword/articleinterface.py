from oneword.models import Article,Comment,MyFavorite,MyLike
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError,ObjectDoesNotExist



# 返回文章列表接口
def allarticle(request):

    if request.method == 'GET':
        article_list=[]
        all_article = Article.objects.all()
        for article in all_article:
            data = {}
            data['author'] = article.author.username
            data['title'] = article.title
            data['tag'] = article.tag
            article_list.append(data)

        return JsonResponse({'status':200,'article_list':article_list,'message':'success'})
    return JsonResponse({'status':10023,'message':'Please use GET method'})


# 根据作者返回文章信息接口
def get_article_author(request):

    if request.method == 'GET':
        author = request.GET.get('author','')

        if author == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        articles = Article.objects.filter(author__username = author.lower())
        article_list=[]
        if articles:
            for article in articles:
                data = {}
                data['title'] = article.title
                data['tag'] = article.tag
                data['id'] = article.id
                article_list.append(data)
            return JsonResponse({'status':200,'data':article_list,'author':author,'message':'success'})
        return JsonResponse({'status':10022,'message':'No result'})
    return JsonResponse({'status':10023,'message':'Please use GET method'})

# 根据文章名称返回文章信息
def get_article_title(request):

    if request.method == 'GET':
        title = request.GET.get('title','')

        if title == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        articles = Article.objects.filter(title__contains = title.lower())
        article_list=[]
        if articles:
            for article in articles:
                data={}
                data['title'] = article.title
                data['author'] = article.author.username
                data['tag'] = article.tag
                data['id'] = article.id
                article_list.append(data)
            return JsonResponse({'status':200,'data':article_list,'message':'success'})
        return JsonResponse({'status':10022,'message':'No result'})
    return JsonResponse({'status':10023,'message':'Please use GET method'})

# 根据文章tag返回文章信息
def get_article_tag(request):

    tag = request.GET.get('tags','')

    if tag == '':
        return JsonResponse({'status':10021,'message':'parameter error'})

    articles = Article.objects.filter(tag__contains = tag.lower())
    article_list=[]
    if articles:
        for article in articles:
            data={}
            data['title'] = article.title
            data['author'] = article.author.username
            data['tag'] = article.tag
            data['id'] = article.id
            article_list.append(data)
        return JsonResponse({'status':200,'data':article_list,'message':'success'})
    return JsonResponse({'status':10022,'message':'No result'})


# 判断是否是自己的文章
@login_required
def my_own_article(request):
    if request.method == 'GET':
        id = request.GET.get('id','')
        user = request.user

        if id and user:
            article = Article.objects.get(id=id)
            if article.author == user:
                return JsonResponse({'status':200,'message':'this is your own article'})
            else:
                return JsonResponse({'status':10022,'message':'this is not your article'})
        else:
            return JsonResponse({'status':10021,'message':'parameter error'})

    return JsonResponse({'status':10023,'message':'not GET method'})


# 收藏文章接口
@login_required
def article_favorite(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id','')
        user = request.user

        if not user:
            return JsonResponse({'status':10021,'message':'Please sign in first'})

        if id == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        # 添加收藏
        article = Article.objects.get(id=id)
        if article.author != user:
            # user = User.objects.get(username=username)
            myfavorite = MyFavorite.objects.get(collector=user)
            if article not in myfavorite.collection.all():
                myfavorite.collection.add(article)
                myfavorite.save()
                # 增加收藏数
                article.favorite += 1
                article.save()
                return JsonResponse({'status':200,'article_id':article.id,'favorite':article.favorite,'message':'add dislike success'})
            return JsonResponse({'status':10024,'message':'you have collected this article'})
        else:
            return JsonResponse({'status':10022,'message':'You DO NOT need to collect your own articles'})

    return JsonResponse({'status':10023,'message':'not GET method'})

# 取消收藏文章接口
@login_required
def article_unfavorite(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id','')
        user = request.user

        if not user:
            return JsonResponse({'status':10020,'message':'Please sign in first'})

        if id == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        # 取消收藏
        article = Article.objects.get(id=id)
        if article.author != user:
            # user = User.objects.get(username=username)
            myfavorite = MyFavorite.objects.get(collector=user)
            myfavorite.collection.remove(article)
            myfavorite.save()
            # 减少收藏数
            article.favorite -= 1
            article.save()
            return JsonResponse({'status':200,'article_id':article.id,'favorite':article.favorite,'message':'add dislike success'})
        else:
            return JsonResponse({'status':10022,'message':'You do not need to collect your own articles'})
    return JsonResponse({'status':10023,'message':'not GET method'})
