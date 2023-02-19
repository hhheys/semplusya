from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from googlesheets import get_classes
from bot import create_callback_data

def first_welcome(classes):
    markup = ReplyKeyboardMarkup()
    markup.add(*classes)
    return markup

def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    markup.add("Расписание уроков")
    markup.add("Расписание звонков") 
    return markup

def cancel_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(" ❌ Отменить")
    return markup

def timetable():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("40 минут(ПН)", callback_data=create_callback_data(fn = 'tt', p = '40pn')),
    InlineKeyboardButton("40 минут(ВТ-ПТ)", callback_data=create_callback_data(fn = 'tt', p = '40')),
    InlineKeyboardButton("35 минут", callback_data=create_callback_data(fn = 'tt', p = '35')),
    InlineKeyboardButton("30 минут", callback_data=create_callback_data(fn = 'tt', p = '30')))
    return markup

def other_class(parameter):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Другой класс", callback_data=create_callback_data(fn = 'oth', p = parameter)))
    return markup

def other_class_talbe(parameter):
    classes = get_classes()
    markup = InlineKeyboardMarkup(row_width=3)
    for i in range(0, len(classes)-1,3):
        markup.add(InlineKeyboardButton(classes[i], callback_data=create_callback_data(fn = 'ott', p = str(parameter) + classes[i])),
            InlineKeyboardButton(classes[i+1], callback_data=create_callback_data(fn = 'ott', p = str(parameter) + classes[i+1])))
            
    return markup

def schedule(day_week, class_name = None):
    next_week = False
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Понедельник (след. неделя)']
    if day_week > 3:
        next_week = True
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row_width = 2
    if next_week:
        markup.row(InlineKeyboardButton("Понедельник (след. неделя)", callback_data=create_callback_data(fn = 'ls', p = '5'))) 
        markup.row(InlineKeyboardButton("Понедельник", callback_data=create_callback_data(fn = 'ls', p = '0')),InlineKeyboardButton("Вторник", callback_data=create_callback_data(fn = 'ls', p = '1')))
        markup.row(InlineKeyboardButton("Среда", callback_data=create_callback_data(fn = 'ls', p = '2')),InlineKeyboardButton("Четверг", callback_data=create_callback_data(fn = 'ls', p = '3')))
        markup.row(InlineKeyboardButton("Пятница", callback_data=create_callback_data(fn = 'ls', p = '4')))
    else:
        markup.row(InlineKeyboardButton(days[day_week + 1], callback_data=create_callback_data(fn = 'ls', p = days.index(days[i]))))
        days[days.index(days[day_week + 1])] == None
        for i in days:
            if i != None:
                markup.add(InlineKeyboardButton(days[i], callback_data=create_callback_data(fn = 'ls', p = days.index(days[i]))))
    return markup