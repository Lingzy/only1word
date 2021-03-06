from django.conf.urls import url
from oneword import articleinterface
from oneword import userinfo


urlpatterns = [
    url(r'^all_list/', articleinterface.allarticle,name='article_list'),
    url(r'^author_search/',articleinterface.get_article_author,name='get_article_author'),
    url(r'^title_search/',articleinterface.get_article_title,name='get_article_title'),
    url(r'^tag_search/',articleinterface.get_article_tag,name='get_article_tag'),
    url(r'^myownarticle/', articleinterface.my_own_article,name='my_own_article'),
    url(r'^is_title_used/', articleinterface.is_title_used,name='title_vaild'),
    url(r'^create_article/', articleinterface.create,name='create_articel'),
    url(r'^add_comment/', articleinterface.add_comment,name='add_comment'),
    url(r'^favorite/', articleinterface.article_favorite,name='favorite'),
    url(r'^unfavorite/', articleinterface.article_unfavorite,name='unfavorite'),
    url(r'^sign/',userinfo.sign,name = 'user_sign'),
    url(r'^register/',userinfo.register,name='user_register'),
    url(r'^logout/',userinfo.userlogout,name='user_logout'),
    url(r'^changepwd/',userinfo.change_pwd,name='changepwd'),
    url(r'^test_tab', articleinterface.test_tab),
]
