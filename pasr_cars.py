from bs4 import BeautifulSoup as bs
import requests
import json

URL = 'https://www.mashina.kg/'

html = requests.get(URL).text
soup = bs(html, 'lxml')

# Легковые авто
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

# Коммерческие авто
commercicals = soup.find('div', class_='category-block commercial').find_all('div', class_='category-block-content-item')
commercical_list = []

for commercical in commercicals:
    name = commercical.find('div', class_='main-title').text.strip()
    price = commercical.find('span', class_='currency-1').text.strip()
    img = commercical.find('img', class_='lazy-image-attr').get('src')
    link = 'https://www.mashina.kg' + commercical.find('a').get('href')

    html = requests.get(link).text
    soup1 = bs(html, 'lxml')
    description = soup1.find('span', class_='original').text.strip().replace('\n', ' ')

    commercical_list.append({
        "Название": name,
        "Цена": price,
        "Изображение": img,
        "Ссылка": link,
        "Описание": description
    })

# Спецтехника
specs = soup.find('div', class_='category-block spec').find_all('div', class_='category-block-content-item')
spec_list = []

for spec in specs:
    name = spec.find('div', class_='main-title').text.strip().replace('\n                                                                    ', ' ')
    price = spec.find('span', class_='currency-1').text.strip()
    img = spec.find('img', class_='lazy-image-attr').get('src')
    link = 'https://www.mashina.kg' + spec.find('a').get('href')

    html = requests.get(link).text
    soup1 = bs(html, 'lxml')
    description = soup1.find('span', class_='original').text.strip().replace('\n', ' ').replace('\r', ' ')

    spec_list.append({
        "Название": name,
        "Цена": price,
        "Изображение": img,
        "Ссылка": link,
        "Описание": description
    })

# Запчасти
parts = soup.find('div', class_='category-block parts').find_all('div', class_='category-block-content-item')
parts_list = []

for part in parts:
    name = part.find('div', class_='main-title').text.strip().replace('\n                                                                    ', ' ')
    try:
        price = part.find('span', class_='currency-1').text.strip()
    except:
        price = "Договорная"
    img = part.find('img', class_='lazy-image-attr').get('src')
    link = 'https://www.mashina.kg' + part.find('a').get('href')

    html = requests.get(link).text
    soup1 = bs(html, 'lxml')
    description = soup1.find('p', class_='comment').text.strip().replace('\n', ' ')

    parts_list.append({
        "Название": name,
        "Цена": price,
        "Изображение": img,
        "Ссылка": link,
        "Описание": description
    })


data_car = {
    "Легковые авто": car_list,
    "Коммерческие авто": commercical_list,
    "Спецтехника": spec_list,
    "Запчасти": parts_list
}

with open("datd.json", "w") as file:
    json.dump(data_car, file, ensure_ascii=False, indent=2)
