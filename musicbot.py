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
    # вызов главного меню
    markup = utils.menu()
    bot.send_message(message.chat.id, 'Добро пожаловать!\nНажмите <b>Начать игру</b> и попробуйте угадать мелодию!', parse_mode='html', reply_markup=markup)

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
        elif message.text == 'Cтатистика':
            Res = utils.return_res(message.chat.id)
            bot.send_message(message.chat.id, 'Ваш cчет: ' + str(Res))
        else:
            bot.send_message(message.chat.id, 'Чтобы начать игру, напишите команду /game')
            

    else:
        # Уберём клавиатуру с вариантами ответа, и вернём предыдущую.
        markup = utils.menu()
        # Если ответ правильный/неправильный
        if message.text == answer:
            bot.send_message(message.chat.id, 'Верно', reply_markup=markup)
            res = True
        else:
            bot.send_message(message.chat.id, 'Не верно. Попробуйте еще раз!', reply_markup=markup)
            res = False
        utils.remove_res(message.chat.id, res)
        # Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)

if __name__ == '__main__':
    random.seed()
    bot.infinity_polling()

