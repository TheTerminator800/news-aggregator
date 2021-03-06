from ...models import Headline
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta

def getslate(per_site):
    url = 'https://slate.com/news-and-politics'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find('div', class_='topic-stories-list').find_all('a')
    i = 0
    for art in articles:
        if i < per_site:
            headline = Headline()

            headline.leaning = 'left'
            headline.url = art['href']
            try:
                headline.title = art.find('span').text
            except AttributeError:
                headline.delete()
                continue
            headline.img = art.find('img')['data-src']

            pub_date = datetime.strptime(art.find('span', class_="topic-story__date").text, '%B %d, %Y')
            if pub_date < datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day):
                headline.mins_ago = 1441
            else:
                pub_time = art.find('div', class_='topic-story__byline').text.strip()[-8:].strip()
                pub_time = datetime.strptime(pub_time, '%I:%M %p').time()
                
                delta = datetime.now() - timedelta(hours=pub_time.hour, minutes=pub_time.minute, seconds=pub_time.second)
                headline.mins_ago = delta.hour*60 + delta.minute

            headline.save()
            i += 1

        else:
            break

