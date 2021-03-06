# Generated by Django 3.1.2 on 2020-11-06 22:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name': 'News Category',
                'verbose_name_plural': 'News Categories',
            },
        ),
        migrations.CreateModel(
            name='NewsProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('website', models.URLField(unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name': 'News Provider',
                'verbose_name_plural': 'News Providers',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField(max_length=500, null=True)),
                ('headline', models.CharField(max_length=250)),
                ('url', models.URLField(max_length=500, unique=True)),
                ('published_on', models.DateTimeField()),
                ('story_excerpt', models.CharField(blank=True, max_length=500)),
                ('story_content', models.TextField()),
                ('story_img', models.URLField(max_length=500, null=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.newscategory')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.newsprovider')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'ordering': ['-published_on'],
            },
        ),
    ]
