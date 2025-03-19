from bs4 import BeautifulSoup as bs
import requests
import json

page = int(input('Какую страницу вы хотите спарсить? '))
if page < 1:
    print('Номер страницы должен быть больше 0. Попробуйте снова.')

URL = 'https://www.kivano.kg/mobilnye-telefony'

if page > 1:
    page_url = f"{URL}?page={page}"
else:
    page_url = URL

response = requests.get(page_url)
html = response.text
soup = bs(html, 'lxml')
telephone_list = soup.find_all('div', class_='item product_listbox oh')

telephones = []
numbering = 0

for telephone in telephone_list:
    title = telephone.find("div", class_="listbox_title").text.strip()
    price = telephone.find("div", class_="listbox_price").text.strip()
    photo = 'https://www.kivano.kg' + telephone.find('img').get('src')
    numbering += 1

    telephones.append({
        "Номер": numbering,
        "Название": title,
        "Цена": price,
        "Описание": photo
    })

with open("db.json", "w") as file:
    json.dump(telephones, file, ensure_ascii=False, indent=2)

# ensure_ascii=False - позволяет сохранять символы в их оригинальном виде, а не в виде ASCII кодов.
# indent - задает отступы для улучшения читаемости JSON файла.
