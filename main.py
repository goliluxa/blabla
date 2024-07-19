import os
import time
import telebot
from telebot import types
import config
import pandas as pd
import csv
from datetime import datetime
from multiprocessing import Process

bot = telebot.TeleBot(config.token)



def analis_data():
    # import config
    while True:
        df1 = pd.read_csv('data/active_trips.csv')

        now = datetime.now()

        for index, row in df1.iterrows():
            try:
                if row['message_id'] == -1:
                    emoji = ''
                    if row['trip_type'] == 'Водитель':
                        emoji = '🚗'
                    elif row['trip_type'] == 'Попутчик':
                        emoji = '🙋‍♂️'
                    elif row['trip_type'] == 'Совместное такси / Каршеринг':
                        emoji = '🚕'
                    extra_flags = row['description_trip'].split(".")
                    if row['trip_type'] == 'Совместное такси / Каршеринг':
                        message_id_ = bot.send_message(-1002201873715, text=f"{emoji} {row['trip_type']} {emoji}\n\n"
                                                                            f"Откуда: {row['from_city']}\n"
                                                                            f"Куда: {row['end_city']}\n\n"
                                                                            f"Дата: {row['date_trip'].replace('=', '.')}\n"
                                                                            f"Время: {row['time_trip'].replace('=', ':')}\n\n"
                                                                            f"Счёт пополам\n\n"
                                                                            f"Автор: @{get_user_info(row['user_id'])['alies']}\n"
                                                                            f"<a href='https://t.me/poputi_inno_bot?start=profile_{row['user_id']}'>Профиль автора</a>\n",
                                                       parse_mode="html").message_id

                    elif row['trip_type'] == 'Водитель':

                        try:
                            link = read_flag(str(row['user_id']) + "link")
                            del_flag(str(row['user_id']) + "link")


                            message_id_ = bot.send_message(-1002201873715, text=f"{emoji} {row['trip_type']} {emoji}\n\n"
                                                                                f"Откуда: {row['from_city']}\n"
                                                                                f"Куда: {row['end_city']}\n\n"
                                                                                f"<a href='{link}'>Ссылка на маршрут</a>\n\n"
                                                                                f"Дата: {row['date_trip'].replace('=', '.')}\n\n"
                                                                                f"Время: {row['time_trip'].replace('=', ':')}\n\n"
                                                                                f"багаж: {extra_flags[0]}\n"
                                                                                f"детское кресло: {extra_flags[1]}\n\n"
                                                                                f"Цена <strong>{row['price_trip']}</strong>\n\n"
                                                                                f"Автор: @{get_user_info(row['user_id'])['alies']}\n"
                                                                                f"<a href='https://t.me/poputi_inno_bot?start=profile_{row['user_id']}'>Открыть профиль автора</a>\n",
                                                           parse_mode="html").message_id
                        except:
                            message_id_ = bot.send_message(-1002201873715, text=f"{emoji} {row['trip_type']} {emoji}\n\n"
                                                                                f"Откуда: {row['from_city']}\n"
                                                                                f"Куда: {row['end_city']}\n\n"
                                                                                f"Дата: {row['date_trip'].replace('=', '.')}\n"
                                                                                f"Время: {row['time_trip'].replace('=', ':')}\n\n"
                                                                                f"багаж: {extra_flags[0]}\n"
                                                                                f"детское кресло: {extra_flags[1]}\n"
                                                                                f"домашнее животное: {extra_flags[2]}\n\n"
                                                                                f"Цена <strong>{row['price_trip']}</strong>\n\n"
                                                                                f"Автор: @{get_user_info(row['user_id'])['alies']}\n"
                                                                                f"<a href='https://t.me/poputi_inno_bot?start=profile_{row['user_id']}'>Профиль автора</a>\n",
                                                           parse_mode="html").message_id
                    elif row['trip_type'] == 'Попутчик':
                        message_id_ = bot.send_message(-1002201873715, text=f"{emoji} {row['trip_type']} {emoji}\n\n"
                                                                            f"Откуда: {row['from_city']}\n"
                                                                            f"Куда: {row['end_city']}\n\n"
                                                                            f"Дата: {row['date_trip'].replace('=', '.')}\n"
                                                                            f"Время: {row['time_trip'].replace('=', ':')}\n\n"
                                                                            f"багаж: {extra_flags[0]}\n"
                                                                            f"детское кресло: {extra_flags[1]}\n"
                                                                            f"домашнее животное: {extra_flags[2]}\n\n"
                                                                            f"Цена <strong>{row['price_trip']}</strong>\n\n"
                                                                            f"Автор: @{get_user_info(row['user_id'])['alies']}\n"
                                                                            f"<a href='https://t.me/poputi_inno_bot?start=profile_{row['user_id']}'>Профиль автора</a>\n",
                                                       parse_mode="html").message_id

                    df1.loc[index, 'message_id'] = message_id_

                date_trip = datetime.strptime(row['date_trip'], '%d=%m=%Y')
                time_trip = datetime.strptime(row['time_trip'], '%H=%M').time()
                trip_datetime = datetime.combine(date_trip, time_trip)
            except:
                try:
                    bot.delete_message(-1002201873715, row['message_id'])
                except Exception as Ex:
                    continue
                df1 = archived_trip(df1, row['unic_trip_id'])

            if trip_datetime < now:
                try:
                    bot.delete_message(-1002201873715, row['message_id'])
                except Exception as Ex:
                    continue
                df1 = archived_trip(df1, row['unic_trip_id'])

        df1.to_csv('data/active_trips.csv', index=False)
        time.sleep(3)


# ============================== Логи ==============================
def write_log(user_id, username, action):
    try:
        with open("data/logs.csv", mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["user_id", 'username', "action"])
            data_ = {
                "user_id": user_id,
                'username': username,
                "action": action.replace("\n", " ")
            }
            writer.writerow(data_)
    except:
        with open("data/logs.csv", mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["user_id", 'username', "action"])
            data_ = {
                "user_id": user_id,
                'username': username,
                "action": action
            }
            writer.writerow(data_)


def read_for_del_mes(user_id):
    try:
        df = pd.read_csv('data/need_to_del_mes.csv')
        flag = df[df['user_id'] == user_id]['message_id'].tolist()
        return flag
    except:
        pass


def write_for_del_mes(user_id, message_id):
    df = pd.read_csv('data/need_to_del_mes.csv')
    new_row = pd.DataFrame({'user_id': [user_id], 'message_id': [message_id]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('data/need_to_del_mes.csv', index=False)


def del_for_del_mes(user_id):
    df = pd.read_csv('data/need_to_del_mes.csv')
    df = df[df['user_id'] != user_id]
    df.to_csv('data/need_to_del_mes.csv', index=False)


def do_del_mes(user_id):
    messages_id_to_del = read_for_del_mes(user_id=user_id)
    if messages_id_to_del:
        for message_id_to_del in messages_id_to_del:
            try:
                bot.delete_message(user_id, message_id_to_del)
            except:
                pass
    del_for_del_mes(user_id)


# ============================== Пользователь ==============================
def add_user(user_id, alies):
    user_data = pd.DataFrame({
        "user_id": [user_id],
        "name": ['Неизвестный'],
        "alies": [alies],
        'photo_id': ['-1'],
        'phone_number': ['Неизвестный'],
        'car': ['Нет информации']
    })

    user_data.to_csv("data/users_data.csv", mode='a', header=False, index=False, encoding='utf-8')


def edit_user_name(user_id, name):
    users = pd.read_csv("data/users_data.csv", encoding='utf-8')
    users.loc[users['user_id'] == user_id, 'name'] = name
    users.to_csv("data/users_data.csv", index=False, encoding='utf-8')

def edit_user_car(user_id, name):
    users = pd.read_csv("data/users_data.csv", encoding='utf-8')
    users.loc[users['user_id'] == user_id, 'car'] = name
    users.to_csv("data/users_data.csv", index=False, encoding='utf-8')

def edit_user_phone_number(user_id, phone_number):
    users = pd.read_csv("data/users_data.csv", encoding='utf-8')
    users.loc[users['user_id'] == user_id, 'phone_number'] = int(phone_number)
    users.to_csv("data/users_data.csv", index=False, encoding='utf-8')


def edit_user_photo_id(user_id, photo_id):
    users = pd.read_csv("data/users_data.csv", encoding='utf-8')
    users.loc[users['user_id'] == user_id, 'photo_id'] = photo_id
    users.to_csv("data/users_data.csv", index=False, encoding='utf-8')


def cheak_new_user(user_id):
    df = pd.read_csv('data/users_data.csv')
    all_ids = df['user_id'].tolist()

    if user_id in all_ids:
        return False
    else:
        return True


def get_user_info(user_id):
    df = pd.read_csv('data/users_data.csv')
    user_info = df[df['user_id'] == user_id]
    return user_info.to_dict('records')[0]


def read_flag(user_id):
    try:
        df = pd.read_csv('data/user_input_flags.csv')
        flag = df[df['user_id'] == user_id]['flag'].tolist()[0]
        return flag
    except:
        pass


def write_flag(user_id, flag_type):
    df = pd.read_csv('data/user_input_flags.csv')
    new_row = pd.DataFrame({'user_id': [user_id], 'flag': [flag_type]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('data/user_input_flags.csv', index=False)


def del_flag(user_id):
    df = pd.read_csv('data/user_input_flags.csv')
    df = df[df['user_id'] != user_id]
    df.to_csv('data/user_input_flags.csv', index=False)


# ============================== поездка ==============================
def get_info_trip(trip_id):
    df = pd.read_csv('data/active_trips.csv')
    trip_info = df[df['trip_id'] == trip_id]
    if trip_info.empty:
        raise ValueError(f"Trip with id {trip_id} not found.")
    else:
        return trip_info


def active_trip(user_id=None, unic_trip_id=None, message_id=None, trip_type=None, from_city=None, end_city=None,
                date_trip=None, time_trip=None, price_trip=None, description_trip=None,
                list_people_id=None, is_verified=None, is_arhive=None, is_users_have_report=None, admins_list=[],
                all_trips=False):
    df = pd.read_csv('data/active_trips.csv')

    def save_to_csv(dataframe):
        dataframe.to_csv('data/active_trips.csv', index=False)

    if all_trips:
        return df.to_dict('records')

    elif unic_trip_id is not None and user_id is None and message_id is None and trip_type is None and from_city is None \
            and end_city is None and date_trip is None and time_trip is None and price_trip is None \
            and description_trip is None and list_people_id is None and is_verified is None \
            and is_arhive is None and is_users_have_report is None:
        result = df[df['unic_trip_id'] == unic_trip_id]
        return result.to_dict('records')

    elif user_id is not None and unic_trip_id is None and message_id is None and trip_type is None and from_city is None \
            and end_city is None and date_trip is None and time_trip is None and price_trip is None \
            and description_trip is None and list_people_id is None and is_verified is None \
            and is_arhive is None and is_users_have_report is None:
        result = df[df['user_id'] == user_id]
        return result.to_dict('records')

    elif unic_trip_id is None:
        new_unic_trip_id = 1
        try:
            max_unic_trip_id = len(df['unic_trip_id'])
            new_unic_trip_id = max_unic_trip_id + 1
        except:
            new_unic_trip_id = 1

        new_data = {
            'user_id': user_id,
            'unic_trip_id': new_unic_trip_id,
            'message_id': message_id,
            'trip_type': trip_type,
            'from_city': from_city,
            'end_city': end_city,
            'date_trip': date_trip,
            'time_trip': time_trip,
            'price_trip': price_trip,
            'description_trip': description_trip,
            'list_people_id': [],
            'is_verified': False,
            'is_arhive': False,
            'is_users_have_report': False,
            'admins_list': admins_list
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        save_to_csv(df)
        return new_unic_trip_id

    elif unic_trip_id is not None:
        mask = (df['unic_trip_id'] == unic_trip_id)
        if mask.any():
            df.loc[mask, 'user_id'] = user_id if user_id is not None else df.loc[mask, 'user_id']
            df.loc[mask, 'message_id'] = message_id if message_id is not None else df.loc[mask, 'message_id']
            df.loc[mask, 'trip_type'] = message_id if message_id is not None else df.loc[mask, 'trip_type']
            df.loc[mask, 'from_city'] = from_city if from_city is not None else df.loc[mask, 'from_city']
            df.loc[mask, 'end_city'] = end_city if end_city is not None else df.loc[mask, 'end_city']
            df.loc[mask, 'date_trip'] = date_trip if date_trip is not None else df.loc[mask, 'date_trip']
            df.loc[mask, 'time_trip'] = time_trip if time_trip is not None else df.loc[mask, 'time_trip']
            df.loc[mask, 'price_trip'] = price_trip if price_trip is not None else df.loc[mask, 'price_trip']
            df.loc[mask, 'description_trip'] = description_trip if description_trip is not None else df.loc[
                mask, 'description_trip']
            df.loc[mask, 'list_people_id'] = list_people_id if list_people_id is not None else df.loc[
                mask, 'list_people_id']
            df.loc[mask, 'is_verified'] = is_verified if is_verified is not None else df.loc[mask, 'is_verified']
            df.loc[mask, 'is_arhive'] = is_arhive if is_arhive is not None else df.loc[mask, 'is_arhive']
            df.loc[mask, 'is_users_have_report'] = is_users_have_report if is_users_have_report is not None else df.loc[
                mask, 'is_users_have_report']
            df.loc[mask, 'admins_list'] = f"{admins_list}"
            save_to_csv(df)
            return


def archived_trip(df=None, unic_trip_id=None, user_id=None):
    df_archived = pd.read_csv('data/archived_trips.csv')

    if df is None and unic_trip_id is None:
        return df_archived.to_dict('records')
    if unic_trip_id is not None and df is None:
        result = df_archived[(df_archived['unic_trip_id'] == unic_trip_id) & (df_archived['user_id'] == user_id)]
        return result.to_dict('records')
    df_active = df

    index_to_move = df_active.index[df_active['unic_trip_id'] == unic_trip_id].tolist()

    trip_to_move = df_active.loc[index_to_move[0]]

    new_unic_trip_id = 1
    try:
        max_unic_trip_id = len(df_archived['unic_trip_id'])
        new_unic_trip_id = max_unic_trip_id + 1
    except:
        new_unic_trip_id = 1

    trip_to_move = trip_to_move.copy()
    trip_to_move['unic_trip_id'] = new_unic_trip_id

    df_active = del_active_trip(df_active, unic_trip_id=unic_trip_id)

    df_archived = pd.concat([df_archived, trip_to_move.to_frame().T], ignore_index=True)

    df_archived.to_csv('data/archived_trips.csv', index=False)
    return df_active


def del_active_trip(df, unic_trip_id):
    df = df[df['unic_trip_id'] != unic_trip_id]
    return df


def split_list(input_list, chunk_size):
    if chunk_size <= 0:
        raise ValueError("chunk_size < 0")

    if len(input_list) <= chunk_size:
        return [input_list]

    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]


def get_cities(except_city=None):
    df = pd.read_csv('data/Cities.csv')
    data = df["name"].tolist()
    if except_city:
        data = [city for city in data if city != except_city]
    return data


def get_name2_by_name(name):
    df = pd.read_csv('data/Cities.csv')
    result = df[df['name'] == name]['name2'].tolist()
    return result[0]


def get_name_by_name2(name2):
    df = pd.read_csv('data/Cities.csv')
    result = df[df['name2'] == name2]['name'].tolist()
    return result[0]


# ============================== главные функции ==============================
@bot.message_handler(commands=['start'])
def start(message, real=True):
    try:
        if message.text.split()[1].split('_')[0] == 'profile':
            data_profile_interface(message, int(message.text.split()[1].split('_')[1]))
        if not cheak_new_user(user_id=message.chat.id):
            bot.delete_message(message.chat.id, message.message_id)

        real = False
    except:
        pass

    if real:
        user_id = message.chat.id
        del_flag(user_id)
        do_del_mes(user_id=user_id)

        if cheak_new_user(user_id=user_id):
            add_user(user_id, message.chat.username)
            message_id = bot.send_message(user_id, f"Открываю").message_id
            menu_interface(message, message_id)
            write_for_del_mes(user_id, message_id)

        else:
            try:
                bot.delete_message(user_id, message.message_id)
            except:
                pass
            message_id = bot.send_message(user_id, f"Открываю").message_id
            menu_interface(message, message_id)
            write_for_del_mes(user_id, message_id)


# ============================== интерфейсы ==============================
def menu_interface(message, message_id):
    del_flag(message.chat.id)
    bottons = types.InlineKeyboardMarkup(row_width=3)

    button_chanel = types.InlineKeyboardButton(f"Канал с поездками 📣", callback_data=f"button_chanel",
                                               url='https://t.me/poputi_innopolis')
    # button_trips = types.InlineKeyboardButton(f"Список поездок 📋", callback_data=f"button_trips")
    button_creat_trip = types.InlineKeyboardButton(f"Создать заявку 📝", callback_data=f"button_creat_trip")
    button_profile = types.InlineKeyboardButton(f"Мой профиль 👤", callback_data=f"button_profile")

    bottons.add(button_chanel)
    bottons.add(button_creat_trip)
    bottons.add(button_profile)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Меню 🗂️",
                          reply_markup=bottons)


def creat_trip_interface(message, message_id):
    if get_user_info(message.chat.id)['photo_id'] == -1 or get_user_info(message.chat.id)['photo_id'] == "-1" or \
            get_user_info(message.chat.id)['name'] == 'Неизвестный':
        bottons = types.InlineKeyboardMarkup(row_width=1)

        button_profile = types.InlineKeyboardButton(f"Мой профиль 👤", callback_data=f"button_profile")
        bottons.add(button_profile)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Сначала заполните все данные профиля",
                              reply_markup=bottons)
    else:
        bottons = types.InlineKeyboardMarkup(row_width=1)

        button_find_trip = types.InlineKeyboardButton(f"Попутчик 🙋‍♂️", callback_data=f"button_find_trip")
        button_new_trip = types.InlineKeyboardButton(f"Водитель 🚗", callback_data=f"button_new_trip")
        button_taxi_trip = types.InlineKeyboardButton(f"Совместное такси / Каршеринг 🚕", callback_data=f"button_taxi_trip")

        bottons.add(button_find_trip)
        bottons.add(button_new_trip)
        bottons.add(button_taxi_trip)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню ⬅️", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Выбор заявки ⬇️",
                              reply_markup=bottons)


def trips_interface(message, message_id, page=0):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню ⬅️", callback_data=f"button_back_to_menu")

    list_of_active_trips = active_trip(all_trips=True)

    split_list_of_active_trips = split_list(list_of_active_trips, 10)

    for i in split_list_of_active_trips[page]:
        emoji = ''
        if i['trip_type'] == 'Водитель':
            emoji = '🚗'
        elif i['trip_type'] == 'Попутчик':
            emoji = '🙋‍♂️'
        elif i['trip_type'] == 'Совместное такси / Каршеринг':
            emoji = '🚕'
        bottons.add(types.InlineKeyboardButton(
            f"{emoji}  {i['from_city']}-{i['end_city']}  {i['date_trip'].replace('=', '.')}  {i['time_trip'].replace('=', ':')}",
            callback_data=f"trip_{i['unic_trip_id']}"))

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

    bottons.add(button_back_to_menu)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Страница {page + 1}",
                          reply_markup=bottons)


def find_trip_interface(message, message_id, step=1, from_city='', end_city='', date_trip='', time_trip='',
                        price_trip='250', extra_flags='🔴.🔴.🔴'):
    if step == 1:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities()
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"f_{get_name2_by_name(i)}")
            bottons.add(button)

        button_creat_trip = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_creat_trip")
        bottons.add(button_creat_trip)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Город отправления ⬇️",
                              reply_markup=bottons)

    elif step == 2:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities(get_name_by_name2(int(from_city)))
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"f_{from_city}_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_new_trip")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Город прибытия ⬇️",
                              reply_markup=bottons)

    elif step == 3:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        cr = '='
        now = datetime.now()
        if date_trip == '':
            date_trip = now.strftime(f"%d{cr}%m{cr}%Y")

        if time_trip == '':
            time_trip = now.strftime(f"%H{cr}%M")

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'timef_{from_city}_{end_city}')

        # ok = types.InlineKeyboardButton(f"Далее ➡️", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"f_{from_city}")

        # bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Укажите дату и время отправления в формате\n"
                                       f"ДД.ММ.ГГГГ ЧЧ:ММ",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 4:
        bottons = types.InlineKeyboardMarkup(row_width=7)

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'pricef_{from_city}_{end_city}_{date_trip}_{time_trip}__')

        # ok = types.InlineKeyboardButton(f"Далее ➡️",
        #                                 callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags}")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"f_{from_city}_{end_city}")
        # bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Укажите стоимость поедки",
                              reply_markup=bottons)


    elif step == 5:

        extra_flags = extra_flags.split('.')

        bottons = types.InlineKeyboardMarkup(row_width=7)

        # багаж, детское кресло, домашнее животное

        bagagh = types.InlineKeyboardButton(f"Багаж {extra_flags[0]}",

                                            callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{'🟢' if extra_flags[0] == '🔴' else '🔴'}.{extra_flags[1]}.{extra_flags[2]}")

        baby_seat = types.InlineKeyboardButton(f"Детское кресло {extra_flags[1]}",

                                               callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{'🟢' if extra_flags[1] == '🔴' else '🔴'}.{extra_flags[2]}")

        animal = types.InlineKeyboardButton(f"Домашнее животное {extra_flags[2]}",

                                            callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}.{'🟢' if extra_flags[2] == '🔴' else '🔴'}")

        ok = types.InlineKeyboardButton(f"Далее ➡️",

                                        callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}.{extra_flags[2]}_")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",

                                                         callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_")

        bottons.add(bagagh)

        bottons.add(baby_seat)

        bottons.add(animal)

        bottons.add(ok)

        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Дополнительные опции к поездки",
                              reply_markup=bottons)

    elif step == 6:

        extra_flags = extra_flags.split('.')

        bottons = types.InlineKeyboardMarkup(row_width=7)

        ok = types.InlineKeyboardButton(f"Разместить✅",

                                        callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}.{extra_flags[2]}__")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",

                                                         callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}.{extra_flags[2]}")

        bottons.add(ok)

        bottons.add(button_back_to_menu)

        # багаж, детское кресло, домашнее животное

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Ваша заявка:\n"
                                   f"🙋‍♂️ Попутчик 🙋‍♂️\n\n"
                                   f"Откуда: {get_name_by_name2(int(from_city))}\n"
                                   f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                                   f"Дата: {date_trip.replace('=', '.')}\n"
                                   f"Время: {time_trip.replace('=', ':')}\n\n"

                                   f"багаж: {extra_flags[0]}\n"

                                   f"детское кресло: {extra_flags[1]}\n"

                                   f"домашнее животное: {extra_flags[2]}\n"

                                   f"Цена <strong>{price_trip}</strong>\n",
                              reply_markup=bottons, parse_mode="html")

    elif step == 7:
        active_trip(user_id=message.chat.id, trip_type="Попутчик", from_city=get_name_by_name2(int(from_city)),
                    end_city=get_name_by_name2(int(end_city)),

                    date_trip=date_trip, time_trip=time_trip, price_trip=int(price_trip),

                    description_trip=extra_flags,

                    list_people_id=[], admins_list=[], is_verified=True, message_id=-1)

        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню ⬅️", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Отправлено ✅",
                              reply_markup=bottons)


def new_trip_interface(message, message_id, step=1, from_city='', end_city='', date_trip='', time_trip='',
                       price_trip='250', extra_flags='🔴.🔴'):
    if step == 1:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities()
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"n_{get_name2_by_name(i)}")
            bottons.add(button)

        button_creat_trip = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_creat_trip")
        bottons.add(button_creat_trip)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Город отправления ⬇️",
                              reply_markup=bottons)

    elif step == 2:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities(get_name_by_name2(int(from_city)))
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"n_{from_city}_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_new_trip")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Город прибытия ⬇️",
                              reply_markup=bottons)

    elif step == 21:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'linkn_{from_city}_{end_city}')

        ok = types.InlineKeyboardButton(f"Далее ➡️", callback_data=f"n_{from_city}_{end_city}_")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"n_{from_city}")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Укажите ссылку на маршрут:\n"
                                       f"(Инструкция по созданию ссылки)",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 3:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        cr = '='
        now = datetime.now()
        if date_trip == '':
            date_trip = now.strftime(f"%d{cr}%m{cr}%Y")

        if time_trip == '':
            time_trip = now.strftime(f"%H{cr}%M")

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'timen_{from_city}_{end_city}')

        # ok = types.InlineKeyboardButton(f"Далее ➡️", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"n_{from_city}")

        # bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Укажите дату и время отправления в формате\n"
                                       f"ДД.ММ.ГГГГ ЧЧ:ММ",
                                  reply_markup=bottons)
        except:
            pass


    elif step == 4:

        bottons = types.InlineKeyboardMarkup(row_width=7)

        del_flag(message.chat.id)

        write_flag(message.chat.id, f'pricen_{from_city}_{end_city}_{date_trip}_{time_trip}__')

        # ok = types.InlineKeyboardButton(f"Далее ➡️",

        #                                 callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags}")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"n_{from_city}_{end_city}")

        # bottons.add(ok)

        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,

                              text=f"Укажите стоимость поедки",

                              reply_markup=bottons)

    elif step == 5:

        extra_flags = extra_flags.split('.')

        print()

        bottons = types.InlineKeyboardMarkup(row_width=7)

        # багаж, детское кресло, домашнее животное

        bagagh = types.InlineKeyboardButton(f"Багаж {extra_flags[0]}",

                                            callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{'🟢' if extra_flags[0] == '🔴' else '🔴'}.{extra_flags[1]}")

        baby_seat = types.InlineKeyboardButton(f"Детское кресло {extra_flags[1]}",

                                               callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{'🟢' if extra_flags[1] == '🔴' else '🔴'}")

        # animal = types.InlineKeyboardButton(f"Домашнее животное {extra_flags[2]}",
        #
        #                                     callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}.{'🟢' if extra_flags[2] == '🔴' else '🔴'}")

        ok = types.InlineKeyboardButton(f"Далее ➡️",

                                        callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}_")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",

                                                         callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}_")

        bottons.add(bagagh)

        bottons.add(baby_seat)

        # bottons.add(animal)

        bottons.add(ok)

        bottons.add(button_back_to_menu)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Напишите описание поездки",
                              reply_markup=bottons)

    elif step == 6:

        extra_flags = extra_flags.split('.')

        bottons = types.InlineKeyboardMarkup(row_width=7)

        ok = types.InlineKeyboardButton(f"Разместить✅",

                                        callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}__")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",

                                                         callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_{extra_flags[0]}.{extra_flags[1]}")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Ваша заявка:\n"
                                   f"🚗 Водитель 🚗\n\n"
                                   f"Откуда: {get_name_by_name2(int(from_city))}\n"
                                   f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                                   f"Дата: {date_trip.replace('=', '.')}\n"
                                   f"Время: {time_trip.replace('=', ':')}\n\n"
                                   f"багаж: {extra_flags[0]}\n"
                                   f"детское кресло: {extra_flags[1]}\n"
                                   f"Цена <strong>{price_trip}</strong>\n",
                              reply_markup=bottons, parse_mode="html")

    elif step == 7:
        active_trip(user_id=message.chat.id, trip_type="Водитель", from_city=get_name_by_name2(int(from_city)),
                    end_city=get_name_by_name2(int(end_city)),

                    date_trip=date_trip, time_trip=time_trip, price_trip=int(price_trip),

                    description_trip=extra_flags,

                    list_people_id=[], admins_list=[], is_verified=True, message_id=-1)

        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню⬅️", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Отправлено✅",
                              reply_markup=bottons)


def taxi_trip_interface(message, message_id, step=1, from_city='', end_city='', date_trip='', time_trip='', extra_flags='🔴.🔴.🔴'):
    if step == 1:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities()
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"t_{get_name2_by_name(i)}")
            bottons.add(button)

        button_creat_trip = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_creat_trip")
        bottons.add(button_creat_trip)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"город отправления ⬇️",
                              reply_markup=bottons)

    elif step == 2:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities(get_name_by_name2(int(from_city)))
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"t_{from_city}_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_taxi_trip")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Город прибытия ⬇️",
                              reply_markup=bottons)

    elif step == 21:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'linkt_{from_city}_{end_city}')

        ok = types.InlineKeyboardButton(f"Далее ➡️", callback_data=f"t_{from_city}_{end_city}_")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"t_{from_city}")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Укажите ссылку на маршрут:\n"
                                       f"(Инструкция по созданию ссылки)",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 3:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        cr = '='
        now = datetime.now()
        if date_trip == '':
            date_trip = now.strftime(f"%d{cr}%m{cr}%Y")

        if time_trip == '':
            time_trip = now.strftime(f"%H{cr}%M")

        del_flag(message.chat.id)
        write_flag(message.chat.id, f'timet_{from_city}_{end_city}')

        # ok = types.InlineKeyboardButton(f"Далее ➡️", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"t_{from_city}")

        # bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Укажите дату и время отправления в формате\n"
                                       f"ДД.ММ.ГГГГ ЧЧ:ММ",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 6:
        # extra_flags = extra_flags.split('.')
        bottons = types.InlineKeyboardMarkup(row_width=7)

        ok = types.InlineKeyboardButton(f"Разместить✅",
                                        callback_data=f"t_{from_city}_{end_city}_{date_trip}_{time_trip}___")

        button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                         callback_data=f"t_{from_city}_{end_city}_{date_trip}_{time_trip}_")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Ваша заявка:\n"
                                   f"🚕 Совместное такси / Каршеринг 🚕\n\n"
                                   f"Откуда: {get_name_by_name2(int(from_city))}\n"
                                   f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                                   f"Дата: {date_trip.replace('=', '.')}\n"
                                   f"Время: {time_trip.replace('=', ':')}\n\n",
                              reply_markup=bottons, parse_mode="html")

    elif step == 7:
        active_trip(user_id=message.chat.id, trip_type="Совместное такси / Каршеринг", from_city=get_name_by_name2(int(from_city)),
                    end_city=get_name_by_name2(int(end_city)),
                    date_trip=date_trip, time_trip=time_trip, price_trip=0,
                    description_trip=extra_flags,
                    list_people_id=[], admins_list=[], is_verified=True, message_id=-1)

        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню ⬅️", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Отправлено ✅",
                              reply_markup=bottons)


def profile_interface(message, message_id, need_del=False):
    if need_del:
        do_del_mes(message.chat.id)
    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_my_activ_trips = types.InlineKeyboardButton(f"Активные поездки ⚡️", callback_data=f"button_my_activ_trips")
    button_my_history_trips = types.InlineKeyboardButton(f"История поездок 📋", callback_data=f"button_my_history_trips")
    button_my_data_profile = types.InlineKeyboardButton(f"Данные профиля 🪪", callback_data=f"button_my_data_profile")
    button_back_to_menu = types.InlineKeyboardButton(f"Назад в меню ⬅️", callback_data=f"button_back_to_menu")

    bottons.add(button_my_activ_trips, button_my_history_trips)
    bottons.add(button_my_data_profile)
    bottons.add(button_back_to_menu)

    if need_del:
        mes_id = bot.send_message(chat_id=message.chat.id,
                              text=f"Профиль меню 👤",
                              reply_markup=bottons).message_id

        write_for_del_mes(message.chat.id, mes_id)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                         text=f"Профиль меню 👤",
                         reply_markup=bottons)


def my_activ_trips_interface(message, message_id, page=0):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    list_of_active_trips = list()

    for i in active_trip(all_trips=True):
        if i['user_id'] == message.chat.id:
            list_of_active_trips.append(i)

    split_list_of_active_trips = split_list(list_of_active_trips, 10)

    for i in split_list_of_active_trips[page]:
        emoji = ''
        if i['trip_type'] == 'Водитель':
            emoji = '🚗'
        elif i['trip_type'] == 'Попутчик':
            emoji = '🙋‍♂️'
        elif i['trip_type'] == 'Совместное такси / Каршеринг':
            emoji = '🚕'
        bottons.add(types.InlineKeyboardButton(
            f"{emoji}  {i['from_city']}-{i['end_city']}  {i['date_trip'].replace('=', '.')}  {i['time_trip'].replace('=', ':')}",
            callback_data=f"my_activ_trip_{i['unic_trip_id']}"))

    if len(split_list_of_active_trips) > 1:
        if page == 0:
            right = types.InlineKeyboardButton(f"▶️", callback_data=f"activ_right_{page + 1}")
            bottons.add(right)
        else:
            left = types.InlineKeyboardButton(f"◀️", callback_data=f"activ_left_{page - 1}")
            if page + 1 < len(split_list_of_active_trips):
                right = types.InlineKeyboardButton(f"️▶️", callback_data=f"activ_right_{page + 1}")
                bottons.add(left, right)
            else:
                bottons.add(left)

    button_back_to_trips_interface = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_profile")

    bottons.add(button_back_to_trips_interface)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Активные поездки",
                          reply_markup=bottons)


def my_history_trips_interface(message, message_id, page=0):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    list_of_active_trips = list()

    for i in archived_trip():
        if i['user_id'] == message.chat.id:
            list_of_active_trips.append(i)

    split_list_of_active_trips = split_list(list_of_active_trips, 10)

    for i in split_list_of_active_trips[page]:
        emoji = ''
        if i['trip_type'] == 'Водитель':
            emoji = '🚗'
        elif i['trip_type'] == 'Попутчик':
            emoji = '🙋‍♂️'
        elif i['trip_type'] == 'Совместное такси / Каршеринг':
            emoji = '🚕'
        bottons.add(types.InlineKeyboardButton(
            f"{emoji}  {i['from_city']}-{i['end_city']}  {i['date_trip'].replace('=', '.')}  {i['time_trip'].replace('=', ':')}",
            callback_data=f"history_trip_{i['unic_trip_id']}"))

    if len(split_list_of_active_trips) > 1:
        if page == 0:
            right = types.InlineKeyboardButton(f"▶️", callback_data=f"history_right_{page + 1}")
            bottons.add(right)
        else:
            left = types.InlineKeyboardButton(f"◀️", callback_data=f"history_left_{page - 1}")
            if page + 1 < len(split_list_of_active_trips):
                right = types.InlineKeyboardButton(f"️▶️", callback_data=f"history_right_{page + 1}")
                bottons.add(left, right)
            else:
                bottons.add(left)

    button_back_to_trips_interface = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_profile")

    bottons.add(button_back_to_trips_interface)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"История поездок",
                          reply_markup=bottons)


def data_profile_interface(message, user_id):
    do_del_mes(user_id=message.chat.id)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_profile_back")

    bottons.add(button_back_to_menu)

    user_data = get_user_info(user_id)
    try:
        if user_data['photo_id'] != "-1":
            mes_id = bot.send_photo(message.chat.id, user_data['photo_id']).message_id
            write_for_del_mes(message.chat.id, mes_id)
    except:
        pass
    mes_id = bot.send_message(chat_id=message.chat.id,
                          text=f"Профиль 👤\n\n"
                               f"ФИО: {user_data['name']}\n"
                               f"Телеграмм: @{user_data['alies']}\n",
                          reply_markup=bottons).message_id

    write_for_del_mes(message.chat.id, mes_id)


def my_data_profile_interface(message):
    do_del_mes(user_id=message.chat.id)

    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_edit_profile_name = types.InlineKeyboardButton(f"Изменить Имя ✍️", callback_data=f"button_edit_profile_name")
    button_edit_profile_phone = types.InlineKeyboardButton(f"Изменить Номер 📞", callback_data=f"button_edit_profile_phone")
    button_edit_profile_photo = types.InlineKeyboardButton(f"Изменить Фото 📸", callback_data=f"button_edit_profile_photo")
    button_edit_profile_car = types.InlineKeyboardButton(f"Изменить Авто 🚘",
                                                           callback_data=f"button_edit_profile_car")
    button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_profile_back")

    bottons.add(button_edit_profile_name)
    bottons.add(button_edit_profile_phone)
    bottons.add(button_edit_profile_photo)
    bottons.add(button_edit_profile_car)
    bottons.add(button_back_to_menu)

    user_data = get_user_info(message.chat.id)
    try:
        if user_data['photo_id'] != "-1":
            mes_id = bot.send_photo(message.chat.id, user_data['photo_id']).message_id
            write_for_del_mes(message.chat.id, mes_id)
    except:
        pass

    mes_id = bot.send_message(chat_id=message.chat.id,
                          text=f"Профиль 👤\n\n"
                               f"ФИО: {user_data['name']}\n"
                               f"Номер телефона: {'+' if user_data['phone_number'] != 'Неизвестный' else ''}{user_data['phone_number']}\n"
                               f"Авто: {user_data['car']}\n"
                               f"Телеграмм: @{user_data['alies']}\n",
                          reply_markup=bottons).message_id

    write_for_del_mes(message.chat.id, mes_id)


def trip_info_interface(message, message_id, trip_id=0, can_edit=False, history=False):
    if can_edit:
        trip_data = active_trip(unic_trip_id=trip_id)[0]
        bottons = types.InlineKeyboardMarkup(row_width=2)

        button_del_my_trip = types.InlineKeyboardButton(f"Удалить поездку ❌", callback_data=f"button_del_my_trip_{trip_id}")
        button_trips = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_my_activ_trips")

        bottons.add(button_del_my_trip)
        bottons.add(button_trips)
    else:
        if history:
            trip_data = archived_trip(unic_trip_id=trip_id, user_id=message.chat.id)[0]
            bottons = types.InlineKeyboardMarkup(row_width=2)

            button_trips = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_my_history_trips")

            bottons.add(button_trips)
        else:
            trip_data = active_trip(unic_trip_id=trip_id)[0]
            bottons = types.InlineKeyboardMarkup(row_width=2)

            button_trips = types.InlineKeyboardButton(f"Назад ⬅️", callback_data=f"button_trips")

            bottons.add(button_trips)

    emoji = ''
    if trip_data['trip_type'] == 'Водитель':
        emoji = '🚗'
    elif trip_data['trip_type'] == 'Попутчик':
        emoji = '🙋‍♂️'
    elif trip_data['trip_type'] == 'Совместное такси / Каршеринг':
        emoji = '🚕'

    if trip_data['trip_type'] == 'Совместное такси / Каршеринг':
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"{emoji} {trip_data['trip_type']} {emoji}\n\n"
                                   f"Откуда: {trip_data['from_city']}\n"
                                   f"Куда: {trip_data['end_city']}\n\n"
                                   f"Дата: {trip_data['date_trip'].replace('=', '.')}\n"
                                   f"Время: {trip_data['time_trip'].replace('=', ':')}\n\n"
                                   f"Описание:\n{trip_data['description_trip']}\n\n",
                              parse_mode="html",
                              reply_markup=bottons)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"{emoji} {trip_data['trip_type']} {emoji}\n\n"
                                   f"Откуда: {trip_data['from_city']}\n"
                                   f"Куда: {trip_data['end_city']}\n\n"
                                   f"Дата: {trip_data['date_trip'].replace('=', '.')}\n"
                                   f"Время: {trip_data['time_trip'].replace('=', ':')}\n\n"
                                   f"Описание:\n{trip_data['description_trip']}\n\n"
                                   f"Цена <strong>{trip_data['price_trip']}</strong>\n",
                              parse_mode="html",
                              reply_markup=bottons)


# ============================== обработка данных ==============================
@bot.message_handler(content_types=['text'])
def message_to_bot(message):
    try:
        user_flag = read_flag(message.chat.id).split('_')[0]
    except:
        user_flag = ''

    try:
        if user_flag == 'Descriptionn':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city, date_trip, time_trip, price_trip = fl.split('_')[1], fl.split('_')[2], fl.split('_')[3], \
                fl.split('_')[4], fl.split('_')[6]

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}__")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Ваше описание:\n\n{message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'Descriptionf':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city, date_trip, time_trip, price_trip = fl.split('_')[1], fl.split('_')[2], fl.split('_')[3], \
                fl.split('_')[4], fl.split('_')[6]

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}__")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Ваше описание:\n\n{message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'Descriptiont':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city, date_trip, time_trip = fl.split('_')[1], fl.split('_')[2], fl.split('_')[3], \
                fl.split('_')[4]

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"t_{from_city}_{end_city}_{date_trip}_{time_trip}___")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"t_{from_city}_{end_city}_{date_trip}_{time_trip}__")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Ваше описание:\n\n{message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'timef':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city = fl.split('_')[1], fl.split('_')[2]

            date_trip, time_trip = message.text.split()[0].replace('.', '='), message.text.split()[1].replace(':', '=')

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"f_{from_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Дата: {message.text.split()[0]}\n"
                                       f"Время: {message.text.split()[1]}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'timet':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city = fl.split('_')[1], fl.split('_')[2]

            date_trip, time_trip = message.text.split()[0].replace('.', '='), message.text.split()[1].replace(':', '=')

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"t_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"t_{from_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Дата: {message.text.split()[0]}\n"
                                       f"Время: {message.text.split()[1]}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'timen':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city = fl.split('_')[1], fl.split('_')[2]

            date_trip, time_trip = message.text.split()[0].replace('.', '='), message.text.split()[1].replace(':', '=')

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"n_{from_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Дата: {message.text.split()[0]}\n"
                                       f"Время: {message.text.split()[1]}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'pricef':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city, date_trip, time_trip = fl.split('_')[1], fl.split('_')[2], fl.split('_')[3], fl.split('_')[4]

            price = message.text

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price}_{'🔴.🔴.🔴'}")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"f_{from_city}_{end_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Цена: {message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'pricen':
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city, date_trip, time_trip = fl.split('_')[1], fl.split('_')[2], fl.split('_')[3], fl.split('_')[4]

            price = message.text

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price}_{'🔴.🔴.🔴'}")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"n_{from_city}_{end_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Цена: {message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'linkn':
            # global links
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city = fl.split('_')[1], fl.split('_')[2]

            link = message.text

            # config.links[message.chat.id] = link
            del_flag(str(message.chat.id) + "link")
            write_flag(str(message.chat.id) + "link", link)
            # print(config.links)

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"n_{from_city}_{end_city}_")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"n_{from_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Ссылка : {message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif user_flag == 'linkt':
            # global links
            bottons = types.InlineKeyboardMarkup(row_width=7)
            fl = read_flag(message.chat.id)
            from_city, end_city = fl.split('_')[1], fl.split('_')[2]

            link = message.text

            # config.links[message.chat.id] = link
            del_flag(str(message.chat.id) + "link")
            write_flag(str(message.chat.id) + "link", link)
            # print(config.links)

            ok = types.InlineKeyboardButton(f"Далее ➡️",
                                            callback_data=f"t_{from_city}_{end_city}_")
            button_back_to_menu = types.InlineKeyboardButton(f"Назад ⬅️",
                                                             callback_data=f"t_{from_city}")

            bottons.add(ok)
            bottons.add(button_back_to_menu)

            bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                                  text=f"Ссылка : {message.text}",
                                  reply_markup=bottons)

            del_flag(message.chat.id)
            write_flag(message.chat.id, message.text)

        elif read_flag(message.chat.id) == 'edit_profile_name':
            edit_user_name(message.chat.id, message.text)
            del_flag(message.chat.id)
            my_data_profile_interface(message)

        elif read_flag(message.chat.id) == 'edit_profile_car':
            edit_user_car(message.chat.id, message.text)
            del_flag(message.chat.id)
            my_data_profile_interface(message)
    except Exception as Ex:
        print(Ex)

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.message_handler(content_types=['photo'])
def message_to_bot(message):
    try:
        if read_flag(message.chat.id) == 'edit_profile_photo':
            edit_user_photo_id(message.chat.id, message.photo[-1].file_id)
            del_flag(message.chat.id)
            my_data_profile_interface(message)
    except:
        pass

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.message_handler(content_types=['contact'])
def message_to_bot(message):
    if read_flag(message.chat.id) == 'edit_profile_phone':
        phone_number = message.contact.phone_number
        edit_user_phone_number(message.chat.id, phone_number)
        del_flag(message.chat.id)
        my_data_profile_interface(message)

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message_id = call.message.message_id
    if call.message:
        if call.data == 'button_creat_trip':
            creat_trip_interface(call.message, message_id)

        elif call.data == 'button_find_trip':
            find_trip_interface(call.message, message_id)

        elif call.data == 'button_new_trip':
            new_trip_interface(call.message, message_id)

        elif call.data == 'button_taxi_trip':
            taxi_trip_interface(call.message, message_id)

        elif call.data == 'button_profile':
            profile_interface(call.message, message_id)

        elif call.data == 'button_profile_back':
            profile_interface(call.message, message_id, need_del=True)

        elif call.data == 'button_back_to_menu':
            menu_interface(call.message, message_id)

        elif call.data.split('_')[0] == 'n':
            print(call.data.split('_'))
            if len(call.data.split('_')[1:]) == 1:
                new_trip_interface(call.message, message_id, 2, call.data.split('_')[1])
            elif len(call.data.split('_')[1:]) == 2:
                new_trip_interface(call.message, message_id, 21, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 3:
                new_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 4:
                new_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 5:
                new_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 6:
                new_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 7:

                new_trip_interface(call.message, message_id, 5, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])
            elif len(call.data.split('_')[1:]) == 8:
                new_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])
            elif len(call.data.split('_')[1:]) == 9:
                new_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2],
                                   call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])

        elif call.data.split('_')[0] == 'f':
            print(call.data.split('_'))
            if len(call.data.split('_')[1:]) == 1:
                find_trip_interface(call.message, message_id, 2, call.data.split('_')[1])
            elif len(call.data.split('_')[1:]) == 2:
                find_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 4:
                find_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 5:
                find_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 6:
                find_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 7:
                find_trip_interface(call.message, message_id, 5, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])
            elif len(call.data.split('_')[1:]) == 8:
                find_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])
            elif len(call.data.split('_')[1:]) == 9:
                find_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6], call.data.split('_')[7])

        elif call.data.split('_')[0] == 't':

            if len(call.data.split('_')[1:]) == 1:
                taxi_trip_interface(call.message, message_id, 2, call.data.split('_')[1])
            elif len(call.data.split('_')[1:]) == 2:
                taxi_trip_interface(call.message, message_id, 21, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 3:
                taxi_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 4:
                taxi_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 5:
                taxi_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 6:
                taxi_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 7:
                taxi_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2],
                                    call.data.split('_')[3], call.data.split('_')[4])
            # elif len(call.data.split('_')[1:]) == 8:
            #     taxi_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2],
            #                         call.data.split('_')[3], call.data.split('_')[4])

        elif call.data == 'button_trips':
            trips_interface(call.message, message_id, 0)

        elif str(call.data).split('_')[0] == "left":
            try:
                trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[1]))
            except:
                pass

        elif str(call.data).split('_')[0] == "right":
            try:
                trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[1]))
            except:
                pass

        elif call.data == 'button_my_activ_trips':
            my_activ_trips_interface(call.message, message_id)

        elif str(call.data).split('_')[0] == "activ" and str(call.data).split('_')[1] == "left":
            try:
                my_activ_trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[2]))
            except:
                pass

        elif str(call.data).split('_')[0] == "activ" and str(call.data).split('_')[1] == "right":
            try:
                my_activ_trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[2]))
            except:
                pass

        elif call.data == 'button_my_history_trips':
            my_history_trips_interface(call.message, message_id)

        elif str(call.data).split('_')[0] == "history" and str(call.data).split('_')[1] == "left":
            try:
                my_history_trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[2]))
            except:
                pass

        elif str(call.data).split('_')[0] == "history" and str(call.data).split('_')[1] == "right":
            try:
                my_history_trips_interface(call.message, call.message.message_id, int(str(call.data).split('_')[2]))
            except:
                pass

        elif call.data == 'button_my_data_profile':
            my_data_profile_interface(call.message)


        elif str(call.data).split('_')[0] == "trip":
            trip_info_interface(call.message, message_id, int(str(call.data).split('_')[1]))

        elif str(call.data).split('_')[0] == "history" and str(call.data).split('_')[1] == "trip":
            trip_info_interface(call.message, message_id, int(str(call.data).split('_')[2]), history=True)

        elif str(call.data).split('_')[0] == "my" and str(call.data).split('_')[1] == "activ" and \
                str(call.data).split('_')[2] == "trip":
            trip_info_interface(call.message, message_id, int(str(call.data).split('_')[3]), can_edit=True)

        elif str(call.data).split('_')[:-1] == 'button_del_my_trip'.split('_'):
            trip_data = active_trip(unic_trip_id=int(str(call.data).split('_')[-1]))[0]
            try:
                bot.delete_message(-1002201873715, trip_data['message_id'])
            except Exception as Ex:
                print(Ex)

            df = pd.read_csv('data/active_trips.csv')

            df = del_active_trip(df, int(str(call.data).split('_')[-1]))

            df.to_csv('data/active_trips.csv', index=False)

            my_activ_trips_interface(call.message, message_id)


        elif str(call.data).split('_') == 'button_edit_profile_name'.split('_'):
            del_flag(call.message.chat.id)
            write_flag(call.message.chat.id, "edit_profile_name")
            do_del_mes(call.message.chat.id)
            mes_id = bot.send_message(chat_id=call.message.chat.id,
                                      text="Напиши имя").message_id
            write_for_del_mes(call.message.chat.id, mes_id)

        elif str(call.data).split('_') == 'button_edit_profile_phone'.split('_'):
            del_flag(call.message.chat.id)
            write_flag(call.message.chat.id, "edit_profile_phone")
            do_del_mes(call.message.chat.id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            markup.add(button_phone)
            mes_id = bot.send_message(chat_id=call.message.chat.id,
                                      text="Отправь номер телефона", reply_markup=markup).message_id
            write_for_del_mes(call.message.chat.id, mes_id)

        elif str(call.data).split('_') == 'button_edit_profile_photo'.split('_'):
            del_flag(call.message.chat.id)
            write_flag(call.message.chat.id, "edit_profile_photo")
            do_del_mes(call.message.chat.id)
            mes_id = bot.send_message(chat_id=call.message.chat.id,
                                      text="Отправь фото").message_id
            write_for_del_mes(call.message.chat.id, mes_id)

        elif str(call.data).split('_') == 'button_edit_profile_car'.split('_'):
            del_flag(call.message.chat.id)
            write_flag(call.message.chat.id, "edit_profile_car")
            do_del_mes(call.message.chat.id)
            mes_id = bot.send_message(chat_id=call.message.chat.id,
                                      text="Напишите информаци об автомобиле\n"
                                           "Цвет, марка, модель, госномер").message_id
            write_for_del_mes(call.message.chat.id, mes_id)


if __name__ == '__main__':
    process = Process(target=analis_data)
    process.start()
    print("Starting bot...\n")
    bot.infinity_polling()
