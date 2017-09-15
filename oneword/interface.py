from oneword.models import Article,Comment,MyFavorite
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.exceptions import ValidationError,ObjectDoesNotExist



# 返回文章列表接口
def allarticle(request):
    article_list=[]
    all_article = Article.objects.all()
    for article in all_article:
        data = {}
        data['author'] = article.author.username
        data['title'] = article.title
        data['tag'] = article.tag
        article_list.append(data)

    return JsonResponse({'status':200,'article_list':article_list,'message':'success'})


# 根据作者返回文章信息接口
def get_article_author(request):
    author = request.POST.get('author','')

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

# 根据文章名称返回文章信息
def get_article_title(request):

    title = request.POST.get('title','')

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

# 喜欢文章接口
def article_like(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id','')
        username = request.session.get('user','')

        if not username:
            return JsonResponse({'status':10020,'message':'Please sign in first'})

        if id == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        # 添加收藏
        article = Article.objects.get(id=id)
        user = User.objects.get(username=username)
        myfavorite = MyFavorite.objects.get(collector=user)
        myfavorite.collection.add(article)
        myfavorite.save()

        # 增加点赞数
        article.like += 1
        article.save()

        return JsonResponse({'status':200,'article_id':article.id,'like':article.like,'message':'add like success'})

    return JsonResponse({'status':10022,'message':'not GET method'})

# 不喜欢文章接口
def article_dislike(request):
    if request.method == 'GET':
        id = request.GET.get('extra_id','')

        if id == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        article = Article.objects.get(id=id)
        article.dislike += 1
        article.save()
        return JsonResponse({'status':200,'article_id':article.id,'dislike':article.dislike,'message':'add dislike success'})
    return JsonResponse({'status':10022,'message':'not GET method'})
