"""only1word URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls import include
from oneword import views,userinfo

# from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$',views.home,name='home'),
    url(r'^accounts/login/$', userinfo.sign),
    url(r'^popular/$', views.popular,name='popular'),
    url(r'^create/$', views.create),
    url(r'^test/$', views.test),
    # url(r'^newar/$', views.newar),
    url(r'^add_comment/$', views.add_comment),
    url(r'^api/', include('oneword.urls',namespace='oneword')),
    url(r'^profiles/$', views.userprofiles,name='profiles'),

    # url('^', include('django.contrib.auth.urls')),
]
