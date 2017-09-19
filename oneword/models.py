from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# 文章模型
class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(blank=False,max_length=60)
    tag = models.CharField(blank=False,max_length=20)
    content = models.TextField(blank=False,max_length=150)
    create_time = models.DateTimeField(auto_now=False)
    like = models.IntegerField(default=0)
    favorite = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# comments模型
class Comment(models.Model):
    author = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    comment = models.TextField(blank=False,max_length=150)
    create_time = models.DateTimeField(auto_now=True)
    like = models.IntegerField(default=0)
    favorite = models.IntegerField(default=0)

    def __str__(self):
        return self.article.title

# 我的收藏
class MyFavorite(models.Model):
    collector = models.ForeignKey(User)
    collection = models.ManyToManyField(Article)

    def __str__(self):
        return self.collector.username

# 我喜欢的文章模型
class MyLike(models.Model):
    collector = models.ForeignKey(User)
    like = models.ManyToManyField(Article)

    def __str__(self):
        return self.collector.username

# 我评论的文章模型
class MyComment(models.Model):
    collector = models.ForeignKey(User)
    comment = models.ManyToManyField(Comment)

    def __str__(self):
        return self.collector.username
