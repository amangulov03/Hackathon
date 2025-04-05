import requests
from bs4 import BeautifulSoup as bs

def get_news():
    URL = 'https://kaktus.media/?lable=8&date=2025-03-17&order=time'
    response = requests.get(URL)
    html = response.text
    soup = bs(html, 'lxml')

    news = soup.find_all('div', class_='Tag--article')[:20]

    parsed_news = []

    for new in news:
        data_time = new.find('div', class_='ArticleItem--time').text.strip()
        description = new.find('a', class_='ArticleItem--name').text.strip()
        link = new.find('a', class_='ArticleItem--name').get('href')
        photo = new.find('img', class_='ArticleItem--image-img').get('src')

        parsed_news.append({
            'time': data_time,
            'description': description,
            'link': link,
            'photo': photo
        })

    return parsed_news

def get_news_details(link):
    response = requests.get(link)
    html = response.text
    soup = bs(html, 'lxml')
    description_block = soup.find('div', class_='BbCode').find('p').text.strip()

    return description_block
