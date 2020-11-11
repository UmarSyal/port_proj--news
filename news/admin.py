from django.contrib import admin
from news import models


# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'category', 'provider', 'published_on', 'created_on')
    list_filter = ('category', 'provider')
    list_per_page = 20
    ordering = ['-published_on']


class NewsProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'website')


admin.site.register(models.NewsProvider, NewsProviderAdmin)
admin.site.register(models.NewsCategory)
admin.site.register(models.News, NewsAdmin)