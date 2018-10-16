# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 02:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='文章标题')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('publishTime', models.DateField(auto_now_add=True)),
                ('modifyTime', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['-publishTime'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='用户名称')),
                ('password', models.CharField(max_length=255, verbose_name='用户密码')),
                ('age', models.IntegerField(default=18, verbose_name='用户年龄')),
                ('nickname', models.CharField(max_length=255, verbose_name='用户昵称')),
                ('birthday', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User'),
        ),
    ]
