import os

from celery.decorators import task
from celery.utils.log import get_task_logger

import scrape

logger = get_task_logger(__name__)

@task(name="scrape_news")
def task_scrape_news():
    """
    Scrapes Latest News
    """
    # temporary solution until heroku paid account not available
    os.system("heroku run python scrape.py")

    # real solution once heroku paid account is available
    # scrape.scrape_news()
    logger.info("News Scrapped")