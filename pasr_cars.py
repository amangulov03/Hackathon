from bs4 import BeautifulSoup as bs
import requests
import json

URL = 'https://www.mashina.kg/'

html = requests.get(URL).text
soup = bs(html, 'lxml')

cars = soup.find('div', class_='category-block cars').find_all('div', class_='category-block-content-item')
car_list = []

for car in cars:
    name = car.find('div', class_='main-title').text.strip()
    price = car.find('span', class_='currency-1').text.strip()
    img = car.find('img', class_='lazy-image-attr').get('src')
    link = 'https://www.mashina.kg' + car.find('a').get('href')

    html = requests.get(link).text
    soup1 = bs(html, 'lxml')
    description = soup1.find('span', class_='original').text.strip().replace('\n', ' ')

    car_list.append({
        "Название": name,
        "Цена": price,
        "Изображение": img,
        "Ссылка": link,
        "Описание": description
    })

data_car = {
    "Легковые авто": car_list
}
with open("datd.json", "w") as file:
    json.dump(data_car, file, ensure_ascii=False, indent=2)
