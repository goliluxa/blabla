import os
import time
import telebot
from telebot import types
from config import *
import pandas as pd
import csv
from datetime import datetime

bot = telebot.TeleBot(token)


# ============================== Логи ==============================
def write_log(user_id, username, action):
    try:
        with open("logs.csv", mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["user_id", 'username', "action"])
            data_ = {
                "user_id": user_id,
                'username': username,
                "action": action.replace("\n", " ")
            }
            # Записываем данные в файл
            writer.writerow(data_)
    except:
        with open("logs.csv", mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["user_id", 'username', "action"])
            data_ = {
                "user_id": user_id,
                'username': username,
                "action": action
            }
            # Записываем данные в файл
            writer.writerow(data_)


def read_for_del_mes(user_id):
    try:
        df = pd.read_csv('need_to_del_mes.csv')
        flag = df[df['user_id'] == user_id]['message_id'].tolist()[0]
        return flag
    except:
        pass


def write_for_del_mes(user_id, message_id):
    df = pd.read_csv('need_to_del_mes.csv')
    new_row = pd.DataFrame({'user_id': [user_id], 'message_id': [message_id]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('need_to_del_mes.csv', index=False)


def del_for_del_mes(user_id):
    df = pd.read_csv('need_to_del_mes.csv')
    df = df[df['user_id'] != user_id]
    df.to_csv('need_to_del_mes.csv', index=False)


# ============================== Пользователь ==============================
def add_user(user_id, name, alies):
    user_data = pd.DataFrame({
        "user_id": [user_id],
        "name": [name],
        "alies": [alies],
        "trips": [0],
        "raiting": [0]
    })

    user_data.to_csv("users_data.csv", mode='a', header=False, index=False, encoding='utf-8')


def edit_user_name(user_id, name):
    users = pd.read_csv("users_data.csv", encoding='utf-8')
    users.loc[users['user_id'] == user_id, 'name'] = name
    users.to_csv("users_data.csv", index=False, encoding='utf-8')


def cheak_new_user(user_id):
    df = pd.read_csv('users_data.csv')
    all_ids = df['user_id'].tolist()

    if user_id in all_ids:
        return False
    else:
        return True


def get_user_info(user_id):
    df = pd.read_csv('users_data.csv')
    user_info = df[df['user_id'] == user_id]
    return user_info.to_dict('records')[0]


def get_lang(user_id):
    df = pd.read_csv('users_lang.csv')
    lang = df[df['user_id'] == user_id]['lang'].tolist()[0]
    return lang


def edit_lang(user_id, lang):
    updated_data = {
        "user_id": user_id,
        "lang": lang
    }
    # Чтение данных из CSV файла в DataFrame
    df = pd.read_csv("users_lang.csv")

    # Проверка, существует ли запись с данным user_id
    if user_id in df['user_id'].values:
        # Обновление данных для указанного user_id
        df.loc[df['user_id'] == user_id, 'lang'] = lang
    else:
        # Добавление новой записи
        new_row = pd.DataFrame([updated_data])
        df = pd.concat([df, new_row], ignore_index=True)

    # Перезапись DataFrame обратно в CSV файл
    df.to_csv("users_lang.csv", index=False)


def read_flag(user_id):
    try:
        df = pd.read_csv('user_input_flags.csv')
        flag = df[df['user_id'] == user_id]['flag'].tolist()[0]
        return flag
    except:
        pass


def write_flag(user_id, flag_type):
    df = pd.read_csv('user_input_flags.csv')
    new_row = pd.DataFrame({'user_id': [user_id], 'flag': [flag_type]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('user_input_flags.csv', index=False)


def del_flag(user_id):
    df = pd.read_csv('user_input_flags.csv')
    df = df[df['user_id'] != user_id]
    df.to_csv('user_input_flags.csv', index=False)


# ============================== поездка ==============================
def get_info_trip(trip_id):
    df = pd.read_csv('active_trips.csv')
    trip_info = df[df['trip_id'] == trip_id]
    if trip_info.empty:
        raise ValueError(f"Trip with id {trip_id} not found.")
    else:
        return trip_info


def new_active_trip(from_city, from_point, to_city, to_point, date, time, places_in_car, car, driver_id):
    df = pd.read_csv('active_trips.csv')
    new_trip_id = df["trip_id"].max() + 1 if not df.empty else 1

    new_trip_data = {
        'trip_id': new_trip_id,
        'from_city': from_city,
        'from_point': from_point,
        'to_city': to_city,
        'to_point': to_point,
        'date': date,
        'time': time,
        'places_in_car': places_in_car,
        'car': car,
        'driver_id': driver_id
    }
    df = df.append(new_trip_data, ignore_index=True)
    df.to_csv('active_trips.csv', index=False)


def new_temp_trip(from_city='~Не заполнено~', from_point='~Не заполнено~', to_city='~Не заполнено~',
                  to_point='~Не заполнено~', date='~Не заполнено~', time='~Не заполнено~',
                  places_in_car='~Не заполнено~', car='~Не заполнено~', driver_id=0):
    df = pd.read_csv('temp_trip.csv')

    if driver_id in df['driver_id'].values:
        if (from_city != '~Не заполнено~' or from_point != '~Не заполнено~' or
                to_city != '~Не заполнено~' or to_point != '~Не заполнено~' or
                date != '~Не заполнено~' or time != '~Не заполнено~' or
                places_in_car != '~Не заполнено~' or car != '~Не заполнено~'):

            if from_city != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['from_city']] = [from_city]

            if from_point != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['from_point']] = [from_point]

            if to_city != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['to_city']] = [to_city]

            if to_point != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['to_point']] = [to_point]

            if date != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['date']] = [date]

            if time != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['time']] = [time]

            if places_in_car != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['places_in_car']] = [places_in_car]

            if car != '~Не заполнено~':
                df.loc[df['driver_id'] == driver_id, ['car']] = [car]
    else:
        new_trip_data = pd.DataFrame({
            'from_city': [from_city],
            'from_point': [from_point],
            'to_city': [to_city],
            'to_point': [to_point],
            'date': [date],
            'time': [time],
            'places_in_car': [places_in_car],
            'car': [car],
            'driver_id': [driver_id]
        })
        df = pd.concat([df, new_trip_data], ignore_index=True)

    df.to_csv('temp_trip.csv', index=False)


def get_temp_trip_info(driver_id):
    df = pd.read_csv('temp_trip.csv')
    trip_info = df[df['driver_id'] == driver_id]
    return trip_info.to_dict('records')[0]


def get_trips_for_panel():
    df = pd.read_csv('active_trips.csv')
    trips = df[["trip_id", 'from_city', 'to_city', 'date', 'time', 'places_in_car']].to_dict(
        orient='records')
    return trips


def split_list(input_list, chunk_size):
    if chunk_size <= 0:
        raise ValueError("chunk_size < 0")

    if len(input_list) <= chunk_size:
        return [input_list]

    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


# ============================== главные функции ==============================
@bot.message_handler(commands=['help'])
def help(message):
    pass


@bot.message_handler(commands=['start'])
def start(message):
    write_log(message.chat.id, message.chat.username, message.text)
    if cheak_new_user(user_id=message.chat.id):
        languages = types.InlineKeyboardMarkup(row_width=1)

        en = types.InlineKeyboardButton(f"English", callback_data=f"edit_lang_on_en")
        ru = types.InlineKeyboardButton(f"Русский", callback_data=f"edit_lang_on_ru")

        languages.add(en)
        languages.add(ru)

        write_for_del_mes(message.chat.id, message.message_id + 1)
        bot.send_message(message.chat.id, f"Выбери язык\n\nChose language", reply_markup=languages)
    else:
        try:
            mes_id_for_del = read_for_del_mes(message.chat.id)
            bot.delete_message(message.chat.id, mes_id_for_del)
            bot.delete_message(message.chat.id, message.message_id)
            del_for_del_mes(message.chat.id)
        except:
            pass

        bot.send_message(message.chat.id, f"Открываю")
        k = 1
        flag = True
        while flag:
            try:
                menu(message, message.message_id + k)
                write_for_del_mes(message.chat.id, message.message_id + k)
                flag = False
            except:
                k += 1


# ============================== интерфейсы ==============================
def after_lang_start(message, message_id):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"напиши Фио")

    del_flag(message.chat.id)
    write_flag(message.chat.id, "FIO")


def after_fio_start(message, message_id, fio):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_name = types.InlineKeyboardButton(f"save_name", callback_data=f"save_name_start")
    edit_name_start = types.InlineKeyboardButton(f"edit_name_start", callback_data=f"edit_name_start")
    bottons.add(save_name, edit_name_start)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Фио: {fio}, оставляем?", reply_markup=bottons)

    del_flag(message.chat.id)
    write_flag(message.chat.id, fio)


def last_start(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    menu = types.InlineKeyboardButton(f"menu", callback_data=f"menu")
    bottons.add(menu)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Вы зарегестрированы\n"
                               f"info: {message.chat.id, read_flag(message.chat.id), message.chat.username}",
                          reply_markup=bottons)

    add_user(message.chat.id, read_flag(message.chat.id), message.chat.username)
    del_flag(message.chat.id)


def menu(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    find_trip = types.InlineKeyboardButton(f"find_trip", callback_data=f"find_trip")
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    profile = types.InlineKeyboardButton(f"profile", callback_data=f"profile")

    bottons.add(find_trip)
    bottons.add(new_trip)
    bottons.add(profile)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"menu",
                          reply_markup=bottons)


def find_trip(message, message_id, page=0):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    filters = types.InlineKeyboardButton(f"filters", callback_data=f"filters")
    menu = types.InlineKeyboardButton(f"back to menu", callback_data=f"menu")
    bottons.add(menu, filters)

    list_of_active_trips = get_trips_for_panel()

    split_list_of_active_trips = split_list(list_of_active_trips, 10)

    for i in split_list_of_active_trips[page]:
        bottons.add(types.InlineKeyboardButton(
            f"{i['from_city']}-{i['to_city']} {i['date']} {i['time']} {i['places_in_car']}",
            callback_data=f"trip_{i['trip_id']}"))
    if len(split_list_of_active_trips) > 1:
        if page == 0:
            right = types.InlineKeyboardButton(f"▶️", callback_data=f"right_{page + 1}")
            bottons.add(right)
        else:
            left = types.InlineKeyboardButton(f"◀️", callback_data=f"left_{page - 1}")
            if page + 1 < len(split_list_of_active_trips):
                right = types.InlineKeyboardButton(f"️▶️", callback_data=f"right_{page + 1}")
                bottons.add(left, right)
            else:
                bottons.add(left)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"page {page + 1}",
                          reply_markup=bottons)


def profile(message, message_id):
    del_flag(message.chat.id)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    edit_name_profile = types.InlineKeyboardButton(f"edit_name_profile", callback_data=f"edit_name_profile")
    history_trips = types.InlineKeyboardButton(f"history_trips", callback_data=f"history_trips")
    menu = types.InlineKeyboardButton(f"menu", callback_data=f"menu")

    bottons.add(edit_name_profile, history_trips)
    bottons.add(menu)

    info_user = get_user_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Профиль:\n"
                               f"ФИО: {info_user['name']}\n"
                               f"Контакт: @{info_user['alies']}",
                          reply_markup=bottons)


def edit_name_profile(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    profile = types.InlineKeyboardButton(f"profile", callback_data=f"profile")
    bottons.add(profile)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "EDIT_FIO")
    info_user = get_user_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_user['name']}\n", reply_markup=bottons)


def save_name_profile(message, message_id, fio):
    del_flag(message.chat.id)
    write_flag(message.chat.id, fio)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_name = types.InlineKeyboardButton(f"save_name_profile", callback_data=f"save_name_profile")
    edit_name_profile = types.InlineKeyboardButton(f"edit_name_profile", callback_data=f"edit_name_profile")

    bottons.add(save_name, edit_name_profile)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {fio}\n", reply_markup=bottons)


def done_name_profile(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    profile = types.InlineKeyboardButton(f"profile", callback_data=f"profile")
    bottons.add(profile)

    fio = read_flag(message.chat.id)
    del_flag(message.chat.id)

    edit_user_name(message.chat.id, fio)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {fio}\n", reply_markup=bottons)


def creat_new_trip(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    edit_from_city = types.InlineKeyboardButton(f"edit_from_city", callback_data=f"edit_from_city")
    edit_from_point = types.InlineKeyboardButton(f"edit_from_point", callback_data=f"edit_from_point")
    edit_to_city = types.InlineKeyboardButton(f"edit_to_city", callback_data=f"edit_to_city")
    edit_to_point = types.InlineKeyboardButton(f"edit_to_point", callback_data=f"edit_to_point")
    edit_date = types.InlineKeyboardButton(f"edit_date", callback_data=f"edit_date")
    edit_time = types.InlineKeyboardButton(f"edit_time", callback_data=f"edit_time")
    edit_places_in_car = types.InlineKeyboardButton(f"edit_places_in_car", callback_data=f"edit_places_in_car")
    edit_car = types.InlineKeyboardButton(f"edit_car", callback_data=f"edit_car")
    # edit_name = types.InlineKeyboardButton(f"edit_name", callback_data=f"edit_name")
    # edit_contact = types.InlineKeyboardButton(f"edit_contact", callback_data=f"edit_contact")

    menu = types.InlineKeyboardButton(f"menu", callback_data=f"menu")
    save_trip = types.InlineKeyboardButton(f"save_trip", callback_data=f"save_trip")

    bottons.add(edit_from_city, edit_to_city)
    bottons.add(edit_from_point, edit_to_point)
    bottons.add(edit_date, edit_time)
    bottons.add(edit_car, edit_places_in_car)
    # bottons.add(edit_name, edit_contact)
    bottons.add(menu, save_trip)

    info_user = get_user_info(message.chat.id)
    new_temp_trip(driver_id=message.chat.id)

    temp_trip_info = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Данные о поездке:\n"
                               f"Город отправления: {temp_trip_info['from_city']}\n"
                               f"Точка отправления: {temp_trip_info['from_point']}\n\n"
                               f"Город прибытия: {temp_trip_info['to_city']}\n"
                               f"Точка прибытия: {temp_trip_info['to_point']}\n\n"
                               f"Дата: {temp_trip_info['date']}\n"
                               f"Время: {temp_trip_info['time']}\n\n"
                               f"Свободно место: {temp_trip_info['places_in_car']}\n\n"
                               f"Данные о водителе:\n"
                               f"ФИО: {info_user['name']}\n"
                               f"Автомобиль: {temp_trip_info['car']}\n"
                               f"Контакт: @{info_user['alies']}",
                          reply_markup=bottons)


def filters(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    by_date = types.InlineKeyboardButton(f"by_date", callback_data=f"by_date")
    by_from_city = types.InlineKeyboardButton(f"by_from_city", callback_data=f"by_from_city")
    by_to_city = types.InlineKeyboardButton(f"by_to_city", callback_data=f"by_to_city")
    by_free_places = types.InlineKeyboardButton(f"by_free_places", callback_data=f"by_free_places")
    clean_filter = types.InlineKeyboardButton(f"clean_filter", callback_data=f"clean_filter")
    back_to_find_trip = types.InlineKeyboardButton(f"back_to_find_trip", callback_data=f"back_to_find_trip")

    bottons.add(back_to_find_trip, clean_filter)
    bottons.add(by_date)
    bottons.add(by_from_city)
    bottons.add(by_to_city)
    bottons.add(by_free_places)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Выберите фильтр",
                          reply_markup=bottons)



# редактор temp_trip
def start_edit_from_city(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_from_city")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['from_city']}\n", reply_markup=bottons)


def save_edit_from_city(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_from_city_temp = types.InlineKeyboardButton(f"save_from_city_temp", callback_data=f"save_from_city_temp")
    edit_from_city_temp = types.InlineKeyboardButton(f"edit_from_city_temp", callback_data=f"edit_from_city_temp")

    bottons.add(save_from_city_temp, edit_from_city_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_from_city(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(from_city=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_to_city(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_to_city")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['to_city']}\n", reply_markup=bottons)


def save_edit_to_city(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_to_city_temp = types.InlineKeyboardButton(f"save_to_city_temp", callback_data=f"save_to_city_temp")
    edit_to_city_temp = types.InlineKeyboardButton(f"edit_to_city_temp", callback_data=f"edit_to_city_temp")

    bottons.add(save_to_city_temp, edit_to_city_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_to_city(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(to_city=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_from_point(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_from_point")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['from_point']}\n", reply_markup=bottons)


def save_edit_from_point(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_from_point_temp = types.InlineKeyboardButton(f"save_from_point_temp", callback_data=f"save_from_point_temp")
    edit_from_point_temp = types.InlineKeyboardButton(f"edit_from_point_temp", callback_data=f"edit_from_point_temp")

    bottons.add(save_from_point_temp, edit_from_point_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_from_point(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(from_point=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_to_point(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_to_point")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['to_point']}\n", reply_markup=bottons)


def save_edit_to_point(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_to_point_temp = types.InlineKeyboardButton(f"save_to_point_temp", callback_data=f"save_to_point_temp")
    edit_to_point_temp = types.InlineKeyboardButton(f"edit_to_point_temp", callback_data=f"edit_to_point_temp")

    bottons.add(save_to_point_temp, edit_to_point_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_to_point(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(to_point=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_date(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_date")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['date']}\n", reply_markup=bottons)


def save_edit_date(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_date_temp = types.InlineKeyboardButton(f"save_date_temp", callback_data=f"save_date_temp")
    edit_date_temp = types.InlineKeyboardButton(f"edit_date_temp", callback_data=f"edit_date_temp")

    bottons.add(save_date_temp, edit_date_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_date(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(date=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_time(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_time")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['time']}\n", reply_markup=bottons)


def save_edit_time(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_time_temp = types.InlineKeyboardButton(f"save_time_temp", callback_data=f"save_time_temp")
    edit_time_temp = types.InlineKeyboardButton(f"edit_time_temp", callback_data=f"edit_time_temp")

    bottons.add(save_time_temp, edit_time_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_time(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(time=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_car(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_car")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['car']}\n", reply_markup=bottons)


def save_edit_car(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_car_temp = types.InlineKeyboardButton(f"save_car_temp", callback_data=f"save_car_temp")
    edit_car_temp = types.InlineKeyboardButton(f"edit_car_temp", callback_data=f"edit_car_temp")

    bottons.add(save_car_temp, edit_car_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_car(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(car=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


def start_edit_places_in_car(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    del_flag(message.chat.id)
    write_flag(message.chat.id, "edit_places_in_car")
    info_temp_trip = get_temp_trip_info(message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Изменить {info_temp_trip['places_in_car']}\n", reply_markup=bottons)


def save_edit_places_in_car(message, message_id, input_data):
    del_flag(message.chat.id)
    write_flag(message.chat.id, input_data)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    save_places_in_car_temp = types.InlineKeyboardButton(f"save_places_in_car_temp", callback_data=f"save_places_in_car_temp")
    edit_places_in_car_temp = types.InlineKeyboardButton(f"edit_places_in_car_temp", callback_data=f"edit_places_in_car_temp")

    bottons.add(save_places_in_car_temp, edit_places_in_car_temp)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранить {input_data}\n", reply_markup=bottons)


def done_edit_places_in_car(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)
    new_trip = types.InlineKeyboardButton(f"new_trip", callback_data=f"new_trip")
    bottons.add(new_trip)

    input_data = read_flag(message.chat.id)
    del_flag(message.chat.id)

    new_temp_trip(places_in_car=input_data, driver_id=message.chat.id)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Сохранено {input_data}\n", reply_markup=bottons)


# ============================== обработка данных ==============================
@bot.message_handler(content_types=['text'])
def message_to_bot(message):
    user_flag = read_flag(message.chat.id)
    if user_flag == "FIO":
        fio = ''
        for i in message.text.split()[:-1]:
            fio += i.capitalize() + " "
        fio += message.text.split()[-1].capitalize()
        k = 1
        flag = True
        while flag:
            try:
                after_fio_start(message, message.message_id - k, fio)
                flag = False
            except:
                k += 1

    elif user_flag == "EDIT_FIO":
        fio = ''
        for i in message.text.split()[:-1]:
            fio += i.capitalize() + " "
        fio += message.text.split()[-1].capitalize()
        k = 1
        flag = True
        while flag:
            try:
                save_name_profile(message, message.message_id - k, fio)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_from_city":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_from_city(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1

    elif user_flag == "edit_to_city":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_to_city(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_from_point":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_from_point(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_to_point":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_to_point(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_date":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_date(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_time":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_time(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1


    elif user_flag == "edit_car":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_car(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1

    elif user_flag == "places_in_car":
        input_data = message.text
        k = 1
        flag = True
        while flag:
            try:
                save_edit_places_in_car(message, message.message_id - k, input_data)
                flag = False
            except:
                k += 1

    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'edit_lang_on_en':
            edit_lang(call.message.chat.id, "en")
            after_lang_start(call.message, call.message.message_id)

        elif call.data == 'edit_lang_on_ru':
            edit_lang(call.message.chat.id, "ru")
            after_lang_start(call.message, call.message.message_id)

        elif call.data == 'edit_name_start':
            after_lang_start(call.message, call.message.message_id)

        elif call.data == 'save_name_start':
            last_start(call.message, call.message.message_id)

        elif call.data in ["find_trip", "back_to_find_trip"]:
            find_trip(call.message, call.message.message_id)

        elif str(call.data).split("_")[0] == "left":
            try:
                find_trip(call.message, call.message.message_id, int(str(call.data).split("_")[1]))
            except:
                pass

        elif str(call.data).split("_")[0] == "right":
            try:
                find_trip(call.message, call.message.message_id, int(str(call.data).split("_")[1]))
            except:
                pass

        elif call.data == "filters":
            filters(call.message, call.message.message_id)

        elif call.data == "menu":
            menu(call.message, call.message.message_id)

        elif call.data == "new_trip":
            creat_new_trip(call.message, call.message.message_id)

        elif call.data == "profile":
            profile(call.message, call.message.message_id)

        elif call.data == "edit_name_profile":
            edit_name_profile(call.message, call.message.message_id)

        elif call.data == "save_name_profile":
            done_name_profile(call.message, call.message.message_id)

        elif call.data == "history_trips":
            pass

        elif call.data == "edit_from_city" or call.data == "edit_from_city_temp":
            start_edit_from_city(call.message, call.message.message_id)

        elif call.data == "edit_to_city" or call.data == "edit_to_city_temp":
            start_edit_to_city(call.message, call.message.message_id)

        elif call.data == "edit_from_point" or call.data == "edit_from_point_temp":
            start_edit_from_point(call.message, call.message.message_id)

        elif call.data == "edit_to_point" or call.data == "edit_to_point_temp":
            start_edit_to_point(call.message, call.message.message_id)

        elif call.data == "edit_date" or call.data == "edit_date_temp":
            start_edit_date(call.message, call.message.message_id)

        elif call.data == "edit_time" or call.data == "edit_time_temp":
            start_edit_time(call.message, call.message.message_id)

        elif call.data == "edit_car" or call.data == "edit_car_temp":
            start_edit_car(call.message, call.message.message_id)

        elif call.data == "edit_places_in_car" or call.data == "edit_places_in_car_temp":
            start_edit_places_in_car(call.message, call.message.message_id)


        elif call.data == "save_from_city_temp":
            done_edit_from_city(call.message, call.message.message_id)


        elif call.data == "save_to_city_temp":
            done_edit_to_city(call.message, call.message.message_id)


        elif call.data == "save_from_point_temp":
            done_edit_from_point(call.message, call.message.message_id)


        elif call.data == "save_to_point_temp":
            done_edit_to_point(call.message, call.message.message_id)


        elif call.data == "save_date_temp":
            done_edit_date(call.message, call.message.message_id)


        elif call.data == "save_time_temp":
            done_edit_time(call.message, call.message.message_id)


        elif call.data == "save_car_temp":
            done_edit_car(call.message, call.message.message_id)


        elif call.data == "save_places_in_car_temp":
            done_edit_places_in_car(call.message, call.message.message_id)




        elif call.data == "save_trip":
            pass


if __name__ == '__main__':
    print("Starting bot...\n")
    bot.infinity_polling()
