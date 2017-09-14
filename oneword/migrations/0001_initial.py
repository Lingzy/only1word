# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-14 01:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('tag', models.CharField(max_length=20)),
                ('content', models.TextField(max_length=150)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=150)),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('like', models.IntegerField(default=0)),
                ('dislike', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oneword.Article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MyFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_time', models.DateTimeField(auto_now=True)),
                ('collection', models.ManyToManyField(to='oneword.Article')),
                ('collector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
