from django.contrib import admin
from oneword.models import Article,Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','author','create_time']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author','create_time']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)

# Register your models here.
