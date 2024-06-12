import os
import time
import telebot
from telebot import types
from config import *
import pandas as pd
import csv
from datetime import datetime

bot = telebot.TeleBot(token)
# -1002201873715

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
        flag = df[df['user_id'] == user_id]['message_id'].tolist()
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
def add_user(user_id, name, alies):
    user_data = pd.DataFrame({
        "user_id": [user_id],
        "name": [name],
        "alies": [alies]
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


def get_cities(except_city=None):
    df = pd.read_csv('Cities.csv')
    data = df["name"].tolist()
    if except_city:
        data = [city for city in data if city != except_city]
    return data


def get_name2_by_name(name):
    df = pd.read_csv('Cities.csv')
    result = df[df['name'] == name]['name2'].tolist()
    return result[0]

def get_name_by_name2(name2):
    df = pd.read_csv('Cities.csv')
    result = df[df['name2'] == name2]['name'].tolist()
    return result[0]

# ============================== главные функции ==============================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    del_flag(user_id)
    do_del_mes(user_id=user_id)

    if cheak_new_user(user_id=user_id):
        add_user(user_id, 1, 1)
        message_id = bot.send_message(user_id, f"Открываю").message_id
        menu_interface(message, message_id)
        write_for_del_mes(user_id, message_id)

    else:
        bot.delete_message(user_id, message.message_id)
        message_id = bot.send_message(user_id, f"Открываю").message_id
        menu_interface(message, message_id)
        write_for_del_mes(user_id, message_id)


@bot.message_handler(commands=['go'])
def go(message):
    bot.send_message(chat_id=-1002201873715,
                          text="текст\n"
                               "<a href='https://t.me/poputi_inno_bot?start=my_action'>link text</a>", parse_mode="html")


# ============================== интерфейсы ==============================
def menu_interface(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_chanel = types.InlineKeyboardButton(f"Канал с поездками", callback_data=f"button_chanel",
                                               url='https://t.me/poputi_innopolis')
    button_find_trip = types.InlineKeyboardButton(f"Хочу уехать", callback_data=f"button_find_trip")
    button_new_trip = types.InlineKeyboardButton(f"Могу подвести", callback_data=f"button_new_trip")
    button_profile = types.InlineKeyboardButton(f"Мой профиль", callback_data=f"button_profile")

    bottons.add(button_chanel)
    bottons.add(button_find_trip, button_new_trip)
    bottons.add(button_profile)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Описание проекта",
                          reply_markup=bottons)


# def find_trip_interface(message, message_id):
#     bottons = types.InlineKeyboardMarkup(row_width=2)
#
#     button_make_get_trip = types.InlineKeyboardButton(f"Создать", callback_data=f"button_make_get_trip")
#     button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")
#
#     bottons.add(button_make_get_trip)
#     bottons.add(button_back_to_menu)
#
#     bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
#                           text=f"Хочу уехать меню",
#                           reply_markup=bottons)
def find_trip_interface(message, message_id, step=1, from_city='', end_city='', date_trip='', time_trip='',
                       price_trip='250'):
    if step == 1:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities()
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"f_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Уеду ОТКУДА",
                              reply_markup=bottons)
    elif step == 2:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities(get_name_by_name2(int(from_city)))
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"f_{from_city}_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"button_new_trip")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Уеду КУДА",
                              reply_markup=bottons)
    elif step == 3:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        cr = '='
        now = datetime.now()
        if date_trip == '':
            date_trip = now.strftime(f"%d{cr}%m{cr}%Y")

        if time_trip == '':
            time_trip = now.strftime(f"%H{cr}%M")

        d = int(date_trip.split(cr)[0])
        m = int(date_trip.split(cr)[1])
        y = int(date_trip.split(cr)[2])

        H = int(time_trip.split(cr)[0])
        M = int(time_trip.split(cr)[1])

        button_space = types.InlineKeyboardButton(f"󠀠󠀠󠁝     ", callback_data=f"1")

        button_1 = types.InlineKeyboardButton(f"Дата", callback_data=f"1")
        button_2 = types.InlineKeyboardButton(f"Время", callback_data=f"1")

        button_point = types.InlineKeyboardButton(f".", callback_data=f"1")
        button_wpoint = types.InlineKeyboardButton(f":", callback_data=f"1")

        def add_but(nums, type_data, add_num):
            nums = nums.split(cr)
            if type_data == 'd':
                nums[0] = str(int(nums[0]) + add_num if 1 <= int(nums[0]) + add_num <= 31 else int(nums[0]))
                if len(nums[0]) == 1:
                    nums[0] = '0' + nums[0]

            elif type_data == 'm':
                nums[1] = str(int(nums[1]) + add_num if 1 <= int(nums[1]) + add_num <= 12 else int(nums[1]))
                if len(nums[1]) == 1:
                    nums[1] = '0' + nums[1]

            elif type_data == 'y':
                nums[2] = str(int(nums[2]) + add_num)

            elif type_data == 'H':
                nums[0] = str(int(nums[0]) + add_num if 0 <= int(nums[0]) + add_num <= 23 else int(nums[0]))
                if len(nums[0]) == 1:
                    nums[0] = '0' + nums[0]

            elif type_data == 'M':
                nums[1] = str(int(nums[1]) + add_num if 0 <= int(nums[1]) + add_num <= 59 else int(nums[1]))
                if len(nums[1]) == 1:
                    nums[1] = '0' + nums[1]

            ret = nums[0]
            for i in nums[1:]:
                ret += cr + i
            return ret

        sp = '󠀠󠀠󠁝     '
        button_up_d = types.InlineKeyboardButton(f"🔼" if d != 31 else sp,
                                                 callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'd', 1)}_{time_trip}")
        button_down_d = types.InlineKeyboardButton(f"🔽" if d != 1 else sp,
                                                   callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'd', -1)}_{time_trip}")

        button_up_m = types.InlineKeyboardButton(f"🔼" if m != 12 else sp,
                                                 callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'm', 1)}_{time_trip}")
        button_down_m = types.InlineKeyboardButton(f"🔽" if m != 1 else sp,
                                                   callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'm', -1)}_{time_trip}")

        button_up_y = types.InlineKeyboardButton(f"🔼",
                                                 callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'y', 1)}_{time_trip}")
        button_down_y = types.InlineKeyboardButton(f"🔽",
                                                   callback_data=f"f_{from_city}_{end_city}_{add_but(date_trip, 'y', -1)}_{time_trip}")

        button_up_H = types.InlineKeyboardButton(f"🔼" if H != 23 else sp,
                                                 callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', 1)}")
        button_down_H = types.InlineKeyboardButton(f"🔽" if H != 0 else sp,
                                                   callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', -1)}")

        button_up_M = types.InlineKeyboardButton(f"🔼" if M != 59 else sp,
                                                 callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', 1)}")
        button_down_M = types.InlineKeyboardButton(f"🔽" if M != 0 else sp,
                                                   callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', -1)}")

        button_plus3h = types.InlineKeyboardButton(f"⬆️ 3ч" if H != 23 else sp,
                                                   callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', 3)}")
        button_minus3h = types.InlineKeyboardButton(f"⬇️ 3ч" if H != 0 else sp,
                                                    callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', -3)}")

        button_plus15m = types.InlineKeyboardButton(f"⬆️ 15м" if M != 59 else sp,
                                                    callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', 15)}")
        button_minus15m = types.InlineKeyboardButton(f"⬇️ 15м" if M != 0 else sp,
                                                     callback_data=f"f_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', -15)}")

        button_d = types.InlineKeyboardButton(f"{d}", callback_data=f"1")
        button_m = types.InlineKeyboardButton(f"{m}", callback_data=f"1")
        button_y = types.InlineKeyboardButton(f"{y}", callback_data=f"1")

        button_H = types.InlineKeyboardButton(f"{H}", callback_data=f"1")
        button_M = types.InlineKeyboardButton(f"{M}", callback_data=f"1")

        bottons.add(button_1)
        bottons.add(button_up_d, button_space, button_up_m, button_space, button_up_y)
        bottons.add(button_d, button_point, button_m, button_point, button_y)
        bottons.add(button_down_d, button_space, button_down_m, button_space, button_down_y)
        bottons.add(button_2)
        bottons.add(button_plus3h, button_up_H, button_space, button_up_M, button_plus15m)
        bottons.add(button_space, button_H, button_wpoint, button_M, button_space)
        bottons.add(button_minus3h, button_down_H, button_space, button_down_M, button_minus15m)

        ok = types.InlineKeyboardButton(f"Готово", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"f_{from_city}")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Уеду КОГДА",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 4:
        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_plus1 = types.InlineKeyboardButton(f"+1",
                                                  callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 1}")
        button_plus10 = types.InlineKeyboardButton(f"+10",
                                                   callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 10}")
        button_plus100 = types.InlineKeyboardButton(f"+100",
                                                    callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 100}")

        button_minus1 = types.InlineKeyboardButton(f"-1",
                                                   callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 1}")
        button_minus10 = types.InlineKeyboardButton(f"-10",
                                                    callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 10}")
        button_minus100 = types.InlineKeyboardButton(f"-100",
                                                     callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 100}")

        button_price = types.InlineKeyboardButton(f"{price_trip}", callback_data=f"1")

        bottons.add(button_minus100, button_minus10, button_minus1, button_price, button_plus1, button_plus10,
                    button_plus100)

        ok = types.InlineKeyboardButton(f"Готово",
                                        callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"f_{from_city}_{end_city}")
        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Уеду ЗА СКОЛЬКО",
                              reply_markup=bottons)

    elif step == 5:

        bottons = types.InlineKeyboardMarkup(row_width=7)
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно",
                                                         callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}_")
        bottons.add(button_back_to_menu)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Уеду НАПИШИ ОПИСАНИЕ",
                              reply_markup=bottons)
        del_flag(message.chat.id)
        write_flag(message.chat.id, f"Descriptionf_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

    elif step == 6:
        bottons = types.InlineKeyboardMarkup(row_width=7)

        ok = types.InlineKeyboardButton(f"Разместить",
                                        callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}___")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно",
                                                         callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Уеду ГОТОВО\n\n"
                                   f"Откуда: {get_name_by_name2(int(from_city))}\n"
                                   f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                                   f"Дата: {date_trip.replace('=', '.')}\n"
                                   f"Время: {time_trip.replace('=', ':')}\n\n"
                                   f"Описание:\n{read_flag(message.chat.id)}",
                              reply_markup=bottons)

    elif step == 7:
        bot.send_message(chat_id=-1002201873715,
                         text=f"Уеду\n\n"
                              f"Откуда: {get_name_by_name2(int(from_city))}\n"
                              f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                              f"Дата: {date_trip.replace('=', '.')}\n"
                              f"Время: {time_trip.replace('=', ':')}\n\n"
                              f"Описание:\n{read_flag(message.chat.id)}\n\n"
                              "<a href='https://t.me/poputi_inno_bot?start=my_action'>Профиль водителя</a>", parse_mode="html")

        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Размещено",
                              reply_markup=bottons)


def new_trip_interface(message, message_id, step=1, from_city='', end_city='', date_trip='', time_trip='', price_trip='250'):
    if step == 1:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities()
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"n_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Подвезу ОТКУДА",
                              reply_markup=bottons)
    elif step == 2:
        bottons = types.InlineKeyboardMarkup(row_width=2)

        Cities_list = get_cities(get_name_by_name2(int(from_city)))
        for i in Cities_list:
            button = types.InlineKeyboardButton(f"{i}", callback_data=f"n_{from_city}_{get_name2_by_name(i)}")
            bottons.add(button)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"button_new_trip")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Подвезу КУДА",
                              reply_markup=bottons)
    elif step == 3:
        bottons = types.InlineKeyboardMarkup(row_width=8)

        cr = '='
        now = datetime.now()
        if date_trip == '':
            date_trip = now.strftime(f"%d{cr}%m{cr}%Y")

        if time_trip == '':
            time_trip = now.strftime(f"%H{cr}%M")

        d = int(date_trip.split(cr)[0])
        m = int(date_trip.split(cr)[1])
        y = int(date_trip.split(cr)[2])

        H = int(time_trip.split(cr)[0])
        M = int(time_trip.split(cr)[1])

        button_space = types.InlineKeyboardButton(f"󠀠󠀠󠁝     ", callback_data=f"1")

        button_1 = types.InlineKeyboardButton(f"Дата", callback_data=f"1")
        button_2 = types.InlineKeyboardButton(f"Время", callback_data=f"1")

        button_point = types.InlineKeyboardButton(f".", callback_data=f"1")
        button_wpoint = types.InlineKeyboardButton(f":", callback_data=f"1")

        def add_but(nums, type_data, add_num):
            nums = nums.split(cr)
            if type_data == 'd':
                nums[0] = str(int(nums[0]) + add_num if 1 <= int(nums[0]) + add_num <= 31 else int(nums[0]))
                if len(nums[0]) == 1:
                    nums[0] = '0' + nums[0]

            elif type_data == 'm':
                nums[1] = str(int(nums[1]) + add_num if 1 <= int(nums[1]) + add_num <= 12 else int(nums[1]))
                if len(nums[1]) == 1:
                    nums[1] = '0' + nums[1]

            elif type_data == 'y':
                nums[2] = str(int(nums[2]) + add_num)

            elif type_data == 'H':
                nums[0] = str(int(nums[0]) + add_num if 0 <= int(nums[0]) + add_num <= 23 else int(nums[0]))
                if len(nums[0]) == 1:
                    nums[0] = '0' + nums[0]

            elif type_data == 'M':
                nums[1] = str(int(nums[1]) + add_num if 0 <= int(nums[1]) + add_num <= 59 else int(nums[1]))
                if len(nums[1]) == 1:
                    nums[1] = '0' + nums[1]

            ret = nums[0]
            for i in nums[1:]:
                ret += cr + i
            return ret


        sp = '󠀠󠀠󠁝     '
        button_up_d = types.InlineKeyboardButton(f"🔼" if d != 31 else sp, callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'd', 1)}_{time_trip}")
        button_down_d = types.InlineKeyboardButton(f"🔽" if d != 1 else sp, callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'd', -1)}_{time_trip}")

        button_up_m = types.InlineKeyboardButton(f"🔼" if m != 12 else sp, callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'm', 1)}_{time_trip}")
        button_down_m = types.InlineKeyboardButton(f"🔽" if m != 1 else sp, callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'm', -1)}_{time_trip}")

        button_up_y = types.InlineKeyboardButton(f"🔼", callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'y', 1)}_{time_trip}")
        button_down_y = types.InlineKeyboardButton(f"🔽", callback_data=f"n_{from_city}_{end_city}_{add_but(date_trip, 'y', -1)}_{time_trip}")

        button_up_H = types.InlineKeyboardButton(f"🔼" if H != 23 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', 1)}")
        button_down_H = types.InlineKeyboardButton(f"🔽" if H != 0 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', -1)}")

        button_up_M = types.InlineKeyboardButton(f"🔼" if M != 59 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', 1)}")
        button_down_M = types.InlineKeyboardButton(f"🔽" if M != 0 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', -1)}")

        button_plus3h = types.InlineKeyboardButton(f"⬆️ 3ч" if H != 23 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', 3)}")
        button_minus3h = types.InlineKeyboardButton(f"⬇️ 3ч" if H != 0 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'H', -3)}")

        button_plus15m = types.InlineKeyboardButton(f"⬆️ 15м" if M != 59 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', 15)}")
        button_minus15m = types.InlineKeyboardButton(f"⬇️ 15м" if M != 0 else sp, callback_data=f"n_{from_city}_{end_city}_{date_trip}_{add_but(time_trip, 'M', -15)}")

        button_d = types.InlineKeyboardButton(f"{d}", callback_data=f"1")
        button_m = types.InlineKeyboardButton(f"{m}", callback_data=f"1")
        button_y = types.InlineKeyboardButton(f"{y}", callback_data=f"1")

        button_H = types.InlineKeyboardButton(f"{H}", callback_data=f"1")
        button_M = types.InlineKeyboardButton(f"{M}", callback_data=f"1")

        bottons.add(button_1)
        bottons.add(button_up_d,        button_space,         button_up_m,        button_space,       button_up_y)
        bottons.add(button_d,           button_point,         button_m,           button_point,       button_y)
        bottons.add(button_down_d,      button_space,         button_down_m,      button_space,       button_down_y)
        bottons.add(button_2)
        bottons.add(button_plus3h,      button_up_H,          button_space,       button_up_M,        button_plus15m)
        bottons.add(button_space,       button_H,             button_wpoint,      button_M,           button_space)
        bottons.add(button_minus3h,     button_down_H,        button_space,       button_down_M,      button_minus15m)

        ok = types.InlineKeyboardButton(f"Готово", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}_ok")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"n_{from_city}")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                                  text=f"Подвезу КОГДА",
                                  reply_markup=bottons)
        except:
            pass

    elif step == 4:
        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_plus1 = types.InlineKeyboardButton(f"+1", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 1}")
        button_plus10 = types.InlineKeyboardButton(f"+10", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 10}")
        button_plus100 = types.InlineKeyboardButton(f"+100", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) + 100}")

        button_minus1 = types.InlineKeyboardButton(f"-1", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 1}")
        button_minus10 = types.InlineKeyboardButton(f"-10", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 10}")
        button_minus100 = types.InlineKeyboardButton(f"-100", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{int(price_trip) - 100}")

        button_price = types.InlineKeyboardButton(f"{price_trip}", callback_data=f"1")

        bottons.add(button_minus100, button_minus10, button_minus1, button_price, button_plus1, button_plus10, button_plus100)

        ok = types.InlineKeyboardButton(f"Готово", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"n_{from_city}_{end_city}")
        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Подвезу ЗА СКОЛЬКО",
                              reply_markup=bottons)

    elif step == 5:

        bottons = types.InlineKeyboardMarkup(row_width=7)
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}_")
        bottons.add(button_back_to_menu)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Подвезу НАПИШИ ОПИСАНИЕ",
                              reply_markup=bottons)
        del_flag(message.chat.id)
        write_flag(message.chat.id, f"Descriptionn_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

    elif step == 6:
        bottons = types.InlineKeyboardMarkup(row_width=7)

        ok = types.InlineKeyboardButton(f"Разместить", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}___")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Подвезу ГОТОВО\n\n"
                                   f"Откуда: {get_name_by_name2(int(from_city))}\n"
                                   f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                                   f"Дата: {date_trip.replace('=', '.')}\n"
                                   f"Время: {time_trip.replace('=', ':')}\n\n"
                                   f"Описание:\n{read_flag(message.chat.id)}",
                              reply_markup=bottons)

    elif step == 7:
        bot.send_message(chat_id=-1002201873715,
                         text=f"Подвезу\n\n"
                              f"Откуда: {get_name_by_name2(int(from_city))}\n"
                              f"Куда: {get_name_by_name2(int(end_city))}\n\n"
                              f"Дата: {date_trip.replace('=', '.')}\n"
                              f"Время: {time_trip.replace('=', ':')}\n\n"
                              f"Описание:\n{read_flag(message.chat.id)}\n\n"
                              "<a href='https://t.me/poputi_inno_bot?start=my_action'>Профиль водителя</a>",
                         parse_mode="html")

        bottons = types.InlineKeyboardMarkup(row_width=7)

        button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                              text=f"Размещено",
                              reply_markup=bottons)


def profile_interface(message, message_id):
    bottons = types.InlineKeyboardMarkup(row_width=2)

    button_my_activ_trips = types.InlineKeyboardButton(f"Активные поездки", callback_data=f"button_my_activ_trips")
    button_my_history_trips = types.InlineKeyboardButton(f"История поездок", callback_data=f"button_my_history_trips")
    button_my_data_profile = types.InlineKeyboardButton(f"Данные профиля", callback_data=f"button_my_data_profile")
    button_back_to_menu = types.InlineKeyboardButton(f"Обратно в меню", callback_data=f"button_back_to_menu")

    bottons.add(button_my_activ_trips, button_my_history_trips)
    bottons.add(button_my_data_profile)
    bottons.add(button_back_to_menu)

    bot.edit_message_text(chat_id=message.chat.id, message_id=message_id,
                          text=f"Профиль меню",
                          reply_markup=bottons)


# ============================== обработка данных ==============================
@bot.message_handler(content_types=['text'])
def message_to_bot(message):
    user_flag = read_flag(message.chat.id).split("_")[0]

    if user_flag == 'Descriptionn':
        bottons = types.InlineKeyboardMarkup(row_width=7)
        fl = read_flag(message.chat.id)
        from_city, end_city, date_trip, time_trip, price_trip = fl.split("_")[1], fl.split("_")[2], fl.split("_")[3], fl.split("_")[4], fl.split("_")[6]

        ok = types.InlineKeyboardButton(f"Готово", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}__")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"n_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                              text=f"Подвезу ПОДТВЕРДИ ОПИСАНИЕ\n{message.text}",
                              reply_markup=bottons)

        del_flag(message.chat.id)
        write_flag(message.chat.id, message.text)

    elif user_flag == 'Descriptionf':
        bottons = types.InlineKeyboardMarkup(row_width=7)
        fl = read_flag(message.chat.id)
        from_city, end_city, date_trip, time_trip, price_trip = fl.split("_")[1], fl.split("_")[2], fl.split("_")[3], fl.split("_")[4], fl.split("_")[6]

        ok = types.InlineKeyboardButton(f"Готово", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}__")
        button_back_to_menu = types.InlineKeyboardButton(f"Обратно", callback_data=f"f_{from_city}_{end_city}_{date_trip}_{time_trip}__{price_trip}_")

        bottons.add(ok)
        bottons.add(button_back_to_menu)

        bot.edit_message_text(chat_id=message.chat.id, message_id=read_for_del_mes(message.chat.id)[0],
                              text=f"Уеду ПОДТВЕРДИ ОПИСАНИЕ\n{message.text}",
                              reply_markup=bottons)

        del_flag(message.chat.id)
        write_flag(message.chat.id, message.text)

    bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message_id = call.message.message_id
    if call.message:
        if call.data == 'button_find_trip':
            find_trip_interface(call.message, message_id)

        elif call.data == 'button_new_trip':
            new_trip_interface(call.message, message_id)

        elif call.data == 'button_profile':
            profile_interface(call.message, message_id)

        elif call.data == 'button_back_to_menu':
            menu_interface(call.message, message_id)

        elif call.data.split('_')[0] == 'n':
            if len(call.data.split('_')[1:]) == 1:
                new_trip_interface(call.message, message_id, 2, call.data.split('_')[1])
            elif len(call.data.split('_')[1:]) == 2:
                new_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 4:
                new_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 5:
                new_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 6:
                new_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 7:
                new_trip_interface(call.message, message_id, 5, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 8:
                new_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 9:
                new_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])

        elif call.data.split('_')[0] == 'f':
            if len(call.data.split('_')[1:]) == 1:
                find_trip_interface(call.message, message_id, 2, call.data.split('_')[1])
            elif len(call.data.split('_')[1:]) == 2:
                find_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2])
            elif len(call.data.split('_')[1:]) == 4:
                find_trip_interface(call.message, message_id, 3, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 5:
                find_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4])
            elif len(call.data.split('_')[1:]) == 6:
                find_trip_interface(call.message, message_id, 4, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 7:
                find_trip_interface(call.message, message_id, 5, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 8:
                find_trip_interface(call.message, message_id, 6, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])
            elif len(call.data.split('_')[1:]) == 9:
                find_trip_interface(call.message, message_id, 7, call.data.split('_')[1], call.data.split('_')[2], call.data.split('_')[3], call.data.split('_')[4], call.data.split('_')[6])


if __name__ == '__main__':
    print("Starting bot...\n")
    bot.infinity_polling()
