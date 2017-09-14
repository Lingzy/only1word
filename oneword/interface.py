from oneword.models import Article,Comment
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
    # title = request.POST.get("title",'')
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

def article_like(request):
    if request.method == 'POST':
        title = request.post.get('title','')

        if title == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        article = Article.objects.get(title=title)
        article.article_likes += 1
        article.save()

def article_dislike(request):
    if request.method == 'POST':
        title = request.post.get('id','')

        if title == '':
            return JsonResponse({'status':10021,'message':'parameter error'})

        article = Article.objects.get(title=title)
        article.article_dislikes += 1
        article.save()
