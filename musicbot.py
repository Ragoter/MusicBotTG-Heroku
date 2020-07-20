# -*- coding: utf-8 -*-
import telebot
import config
import utils
import random
from telebot import types
from SQLighter import SQLighter

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Начать игру')
    markup.add(item)
    bot.send_message(message.chat.id, 'Добро пожаловать!\nНажми <b>Начать игру</b> и попробуй угадать мелодию!', parse_mode='html', reply_markup=markup)
@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Если None:
    if not answer:
        if message.text == "Начать игру":
            # Подключаемся к БД
            db_worker = SQLighter(config.database_name)
            # Получаем слачайную строку из БД
            row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
            # Формируем разметку
            markup = utils.generate_markup(row[2], row[3])
            # отправляем аудиофайл с вариантами ответа
            bot.send_voice(message.chat.id, row[1], reply_markup=markup)
            # Включаем "игровой режим"
            utils.set_user_game(message.chat.id, row[2])
            # Отсоединяемся от БД
            db_worker.close()
        else:
            bot.send_message(message.chat.id, 'Чтобы начать игру, напишите команду /game')
    else:
        # Уберём клавиатуру с вариантами ответа.
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Не верно. Попробуйте еще раз!', reply_markup=keyboard_hider)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)
if __name__ == '__main__':
    random.seed()
    bot.infinity_polling()

