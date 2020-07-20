# -*- coding: utf-8 -*-
import shelve
from config import shelve_name, database_name
from SQLighter import SQLighter 
from random import shuffle
import telebot

def count_rows():
    """
    Данный метод считает общее кол-во строк в базе данных и сохраняет в хранилище.
    Потом из этого кол-ва будем выбирать музыку.
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows
    with shelve.open(shelve_name) as storage:
        print(rowsnum)
        storage['rows_count'] = rowsnum

def get_rows_count():
    """
    Получает из хранилища кол-во строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum

def set_user_game(chat_id, estimated_answer):
    """
    Записываем юзера в игроки и запоминает, что он должен ответить
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer

def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    : param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]

def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера
    В случае, если человек просто ввёл какие-то символ, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answers):
    """
    Создаем кастомную клавиатуру для выбора ответа
    : param right_answer: правильный ответ
    : param wrong_answers: Набор неправильных ответов
    : return: Объект кастомной клавиатуры
    """
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Склеиваем правильный ответ с неправильными
    all_answers = '{},{}'.format(right_answer, wrong_answers)
    # Создаем лист(массив) и записываем в него все элементы
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Перемашаем элементы
    shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    #return markup.add(list_items[0],list_items[1],list_items[2],list_items[3])
    for item in list_items:
        markup.add(item)
    return markup
