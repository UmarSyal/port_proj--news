from dateutil.parser import parse as parse_date
from dateutil.utils import default_tzinfo

import bs4 # pip install bs4

from news import models
from .utils import get_soup, log_scrape, default_tz


def dawn_scrapper(soup, news_provider, last_news_provider):
    """
    go through the soup object obtained from Dawn news scrape call.
    go through all the articles, retrieve required data and
    a list of models.News objects to return
    """
    
    # All News Articles
    tabs = soup.select('div.w-full > div.tabs div.tabs__pane')
    news_list = []
    errors = []

    # go over all the articles
    for tab in tabs:
        if tab['id'].lower() == 'all':
            continue

        articles = tab.select('article.box.story')
        print('Total Articles: ', len(articles))
        
        for index, article in enumerate(articles):
            print('\n', index, end='\t')
            try:
                # get or created the models.NewsProvider object for models.News object
                provider, p_created = models.NewsProvider.objects.get_or_create(
                                                            name=news_provider['name'],
                                                            short_name=news_provider['short_name'],
                                                            website=news_provider['website'])
                provider.save()

                # get or created the models.NewsCategory object for models.News object
                cat = 'Sports' if tab['id'].strip().lower() == 'sport' else tab['id'].strip().capitalize()
                print('cat:', type(cat), end=' ')
                category, c_created = models.NewsCategory.objects.get_or_create(category=cat)
                category.save()

                # thumbnail image
                thumbnail = article.find('div', {'class': 'media__item'}).find('img')['src'].strip()
                
                # headline
                headline = article.find('h2')
                print('headline:', type(headline), end=' ')
                headline = headline.text.strip()

                # url of the story
                url = article.find('h2', {"class": "story__title"})
                url = url.find('a', {"class": "story__link"})['href'].strip()

                # publishing date of the story, use dateutil.parser to
                # convert string date into datetime object
                published_on = article.find('span', {"class": "story__time"})
                published_on = published_on.find('span', {"class": "timestamp--time timeago"})
                print('published_on:', type(published_on), end=' ')
                published_on = parse_date(published_on['title'].strip(), ignoretz=True)
                published_on = default_tzinfo(published_on, default_tz)

                # story excerpt
                story_excerpt = article.find('div', {'class': 'story__excerpt'})
                print('story_excerpt:', type(story_excerpt), end=' ')
                story_excerpt = story_excerpt.decode_contents()

                # make a request to the story's url and get the soup
                story_soup = get_soup(url)

                # story content
                story_content = story_soup.select_one("div.story__content")
                print('story_content:', type(story_content), end=' ')
                story_content = story_content.decode_contents()

                # story image
                story_img = story_soup.select_one('main div.slideshow__slide--first div.media__item')
                if isinstance(story_img, bs4.element.Tag):
                    story_img = story_img.find('img')['src'].strip()
                else:
                    story_img = thumbnail
                    
                # create a new models.News object with all the data
                news, n_created = models.News.objects.get_or_create(category=category,
                                            provider=provider, thumbnail=thumbnail,
                                            headline=headline, url=url, published_on=published_on,
                                            story_excerpt=story_excerpt, 
                                            story_content=story_content, story_img=story_img)
                news.save()
                news_list.append(news)
            except Exception as e:
                errors.append(e)
                print('Error:', e, '=', len(errors))
                continue
            
    print('\nTotal Fetched: ', len(news_list))
    print('Total Errors: ', len(errors))
    log_scrape(news_provider['name'], last_news_provider, len(news_list), len(errors))
    return news_list


if __name__ == "__main__":
    pass