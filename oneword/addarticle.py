from models import Article
from django.contrib.auth.models import User
import time
import random
from datetime import datetime


users = User.objects.all()
tags=['love','magic','dark','tech']

for i in range(100):

    author = random.choice(users)
    title = "Test {0} article".format(i)
    tag = random.choice(tags)
    content = "This is a test article, NO.{0}".format(i)
    create_time = datetime.fromtimestamp(time.time())

    Article.objects.create(author=author,title=title,tag=tag,content=content,create_time=create_time)
