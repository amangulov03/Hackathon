import telebot
from config import TOKEN
from parser import get_news, get_news_details
from keyboards import main_keyboard

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Здравствуйте {message.from_user.first_name}, я могу спарсить новости на сайте kaktus.media.kg\nВот последние 20 новостей:')
    show_news(message)

def show_news(message):
    try:
        news = get_news()
        links = []
        photos = []

        for i, item in enumerate(news):
            links.append(item['link'])
            photos.append(item['photo'])

            bot.send_message(
                message.chat.id,
                f'№{i + 1}\nВремя - <i>{item["time"]}</i>\nОписание - <b>{item["description"]}</b>\nФото: {item["photo"]}',
                parse_mode='html'
            )

        msg = bot.send_message(message.chat.id, 'Выбери номер новости (1-20) или нажми Quit для завершения:', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, select_news, links, photos)

    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при парсинге: {str(e)}')

def select_news(message, links, photos):
    try:
        if message.text == 'Quit':
            bot.send_message(message.chat.id, 'До свидания!', reply_markup=telebot.types.ReplyKeyboardRemove())
            return

        try:
            num = int(message.text)
            if num < 1 or num > 20:
                msg = bot.send_message(message.chat.id, 'Такого номера нет. Введите от 1 до 20 или нажмите Quit.', reply_markup=main_keyboard())
                bot.register_next_step_handler(msg, select_news, links, photos)
                return
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Ошибка. Введите число от 1 до 20 или нажмите Quit.', reply_markup=main_keyboard())
            bot.register_next_step_handler(msg, select_news, links, photos)
            return

        index = num - 1
        description = get_news_details(links[index])
        caption = f'Новость - №{num}\n<b>Описание:</b>\n{description}'
        bot.send_photo(message.chat.id, photos[index], caption=caption, parse_mode='html')

        msg = bot.send_message(message.chat.id, 'Выбери другую новость (1-20) или нажми Quit', reply_markup=main_keyboard())
        bot.register_next_step_handler(msg, select_news, links, photos)

    except Exception:
        msg = bot.send_message(message.chat.id, 'Пожалуйста, введите корректный номер или нажмите Quit.')
        bot.register_next_step_handler(msg, select_news, links, photos)

bot.polling(non_stop=True)
