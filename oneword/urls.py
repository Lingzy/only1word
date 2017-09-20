from django.conf.urls import url
from oneword import articleinterface
from oneword import userinfo


urlpatterns = [
    url(r'^all_list/', articleinterface.allarticle,name='article_list'),
    url(r'^author_search/',articleinterface.get_article_author,name='get_article_author'),
    url(r'^title_search/',articleinterface.get_article_title,name='get_article_title'),
    url(r'^tag_search/',articleinterface.get_article_tag,name='get_article_tag'),
    url(r'^myownarticle/', articleinterface.my_own_article,name='my_own_article'),
    url(r'^like/', articleinterface.article_like,name='like'),
    url(r'^dislike/', articleinterface.article_dislike,name='dislike'),
    url(r'^favorite/', articleinterface.article_favorite,name='favorite'),
    url(r'^unfavorite/', articleinterface.article_unfavorite,name='unfavorite'),
    url(r'^sign/',userinfo.sign,name = 'user_sign'),
    url(r'^register/',userinfo.register,name='user_register'),
    url(r'^logout/',userinfo.userlogout,name='user_logout'),
    url(r'^changepwd/',userinfo.change_pwd,name='changepwd'),
]
