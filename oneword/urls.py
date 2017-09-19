from django.conf.urls import url
from oneword import articleinterface
from oneword import userinfo


urlpatterns = [
    url(r'^all_list/', articleinterface.allarticle,name='article_list'),
    url(r'^author_search/',articleinterface.get_article_author,name='get_article_author'),
    url(r'^title_search/',articleinterface.get_article_title,name='get_article_title'),
    url(r'^like/', articleinterface.article_like,name='like'),
    url(r'^favorite', articleinterface.article_favorite,name='favorite'),
    url(r'^sign/',userinfo.sign,name = 'user_sign'),
    url(r'^register/',userinfo.register,name='user_register'),
    url(r'^logout/',userinfo.userlogout,name='user_logout'),
    url('^changepwd/',userinfo.change_pwd,name='changepwd'),
]
