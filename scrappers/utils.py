from requests_html import HTMLSession # pip install requests-html
import bs4 # pip install bs4
from datetime import datetime


def get_soup(url):
    """
    make a request to a website, use BeautifulSoup to parse the response and
    return the parsed object
    """
    session = HTMLSession()
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    session.close()
    response.close()
    return soup


def log_scrape(news_provider, fetched, errors):
    date_time = str(datetime.now()) + '\n'
    news_provider = news_provider + '\t'
    fetched = 'Total Fetched: ' + str(fetched) + '\t'
    errors = 'Total Errors: ' + str(errors) + '\n'

    with open('scrape_log.txt', 'a') as f:
        f.writelines([
            date_time,
            news_provider,
            fetched,
            errors,
        ])
        if news_provider.strip() == 'Dawn News':
            f.writelines([
                '------------------------------------------------------------\n',
            ])