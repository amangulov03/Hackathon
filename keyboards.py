from telebot import types

def main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Quit')
    keyboard.add(button)
    return keyboard
