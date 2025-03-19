import telebot
from bs4 import BeautifulSoup as bs
import requests

bot = telebot.TeleBot('7992977093:AAEHwDz7ZwoYrxUfoj9yhApGVQQYDDllPig')

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
button = telebot.types.KeyboardButton('Quit')
keyboard.add(button)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Здравствуйте {message.from_user.first_name}, я могу спарсить новости на сайте kaktus.media.kg\nВот последние 20 новостей:')
    pars_news(message)

def pars_news(message):
    try:
        URL = 'https://kaktus.media/?lable=8&date=2025-03-17&order=time'

        response = requests.get(URL)
        html = response.text
        soup = bs(html, 'lxml')
        news = soup.find_all('div', class_='Tag--article')[:20]

        num = 0
        links = []
        for new in news:
            data_time = new.find('div', class_='ArticleItem--time').text.strip()
            descriptions = new.find('a', class_='ArticleItem--name').text.strip()
            link = new.find('a', class_='ArticleItem--name').get('href')
            print(f'Ссылка - {link}')
            photo = new.find('img', class_='ArticleItem--image-img').get('src')
            print(f'Фото - {photo}')
            num += 1
            links.append(link)
            print(links)

            bot.send_message(message.chat.id, f'№{num}\nВремя - <i>{data_time}</i>\nОписания - <b>{descriptions}</b>\nФото: {photo}', parse_mode='html')
        msg = bot.send_message(message.chat.id, 'Выбери номер новости (1-20) или нажми Quit для завершения:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, select_news, links)

    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при парсинге: {str(e)}')

def select_news(message, links):

    try:
        if message.text == 'Quit':
            bot.send_message(message.chat.id, 'До свидания!', reply_markup=telebot.types.ReplyKeyboardRemove())
            return

        try:
            num = int(message.text)
            if num < 1 or num > 20:
                msg = bot.send_message(message.chat.id, 'Такого номера новости нет, введи число от 1 до 20 или нажми Quit', reply_markup=keyboard)
                bot.register_next_step_handler(msg, select_news, links)
                return
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Ошибка, введи число от 1 до 20 или нажми Quit', reply_markup=keyboard)
            bot.register_next_step_handler(msg, select_news, links)
            return

        news_index = num - 1
        selected_link = links[news_index]

        respons = requests.get(selected_link)
        html = respons.text
        soup = bs(html, 'lxml')

        description_block = soup.find('div', class_='BbCode').find('p').text.strip()
        bot.send_message(message.chat.id, f'<b>Описание:</b>\n{description_block}', parse_mode='html')

        msg = bot.send_message(message.chat.id, 'Выбери другую новость (1-20) или нажми Quit', reply_markup=keyboard)
        bot.register_next_step_handler(msg, select_news, links)
    except Exception:
        msg = bot.send_message(message.chat.id, 'Пожалуйста, введите корректный номер или нажми Quit')
        bot.register_next_step_handler(msg, select_news, links)

bot.polling(non_stop=True, interval=0)
