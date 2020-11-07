"""
context_processors for base.html
need these because there is no view associated with base.html
which can pass a context object.

add the functions defined here in settings.py(TEMPLATES.OPTIONS.context_processors)
"""

from news.models import NewsCategory, NewsProvider

def get_news_categories(request):
    """
    get list of categories to show in sidebar filters
    """
    return {'categories': NewsCategory.objects.order_by('category')}


def get_news_providers(request):
    """
    get list of providers to show in sidebar filters
    """
    return {'providers': NewsProvider.objects.order_by('name')}