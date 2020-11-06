# setup django environment
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_scrapper.settings')

import django
django.setup()

from scrappers.br_scrapper import brecorder_scrapper
from scrappers.dawn_scrapper import dawn_scrapper
from scrappers.utils import get_soup


def scrape_news():
    """
    scrapes news from all news providers and saves them in DB
    """
    for news_provider in news_providers:
        soup = get_soup(news_provider['website'])
        news_list = news_provider['scrapper'](soup, news_provider)


news_providers = [
        {
            'name': 'Bussiness Recorder',
            'short_name': 'BR',
            'website': 'https://www.brecorder.com/latest-news',
            'scrapper': brecorder_scrapper, # value is a function
        },
        {
            'name': 'Dawn News',
            'short_name': 'Dawn',
            'website': 'https://www.dawn.com/latest-news',
            'scrapper': dawn_scrapper, # value is a function
        },
    ]


if __name__ == "__main__":
    scrape_news()