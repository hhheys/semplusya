import telebot
from googlesheets import get_classes,get_timetable
import json_manager
import config
import murkups
import datetime
import json

bot = telebot.TeleBot(config.TOKEN)

classes = None

def create_callback_data(**kwargs):
    return json.dumps(kwargs, ensure_ascii=False)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not json_manager.user_exists(message.from_user.id):
        msg = bot.reply_to(message, config.message['first_welcome'],reply_markup=murkups.first_welcome(get_classes()))
        bot.register_next_step_handler(msg, input_class)
    else:
        msg = bot.reply_to(message, config.message['welcome'],reply_markup=murkups.main_keyboard())

@bot.message_handler(commands=['news'])
def create_news(message):
    if json_manager.admin_exists(message.from_user.id):
        msg = bot.reply_to(message, config.message['create_news_title'], reply_markup=murkups.cancel_keyboard())
        bot.register_next_step_handler(msg, send_news)
    else:
        bot.send_message(message.from_user.id, '❗ Вы не являетесь администратором!', reply_markup=murkups.main_keyboard())

def send_news(message):
    if message.text != '❌ Отменить':
        for i in json_manager.get_users():
            bot.send_message(i['tg_id'],message.text, parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id,'Вы вышли из редактора новостей.', reply_markup=murkups.main_keyboard())

def input_class(message):
    if message.text in classes:
        json_manager.add_user(message.from_user.id,message.text)
        bot.reply_to(message, config.message['registration_success'], reply_markup=murkups.main_keyboard())
    else:
        msg = bot.reply_to(message, config.message['wrong_class'], reply_markup=murkups.first_welcome(classes))
        bot.register_next_step_handler(msg, input_class)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Расписание звонков":         
        bot.send_message(message.from_user.id, "👇 Выберите расписание", reply_markup=murkups.timetable())
    elif message.text == "Расписание уроков":         
        bot.send_message(message.from_user.id, config.message['lessons_input_date'].format(config.days[datetime.date.today().weekday()], datetime.date.today()), reply_markup=murkups.schedule(datetime.date.today().weekday()))
    else:
        send_welcome(message)
        


def generate_shedule(day_week, telegram_id = None, class_name = None):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Понедельник (след. неделя)']
    message_shedule = ''
    if class_name == None:
        user_class = json_manager.get_user_class(telegram_id)
    else:
        user_class = class_name
    shedule = get_timetable(day_week, user_class)
    numbers = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣']
    for i in shedule:
        row = ''
        if i[2] == 'Classroom hour':
            row = '🕗  ' + numbers[0] +'         {} ⇒    {} \n'.format(i[1].ljust(15,' '),i[0])# parse_mode="Markdown"
        elif i[2] == 'Changed':
            row = '❗  '+ numbers[0] +'         {} ⇒    {} \n'.format(i[1].ljust(15,' '),i[0])
        elif i[2] == 'Cancelled':
            row = '❌  '+ numbers[0] +'         {} ⇒    {} \n'.format(i[1].ljust(15,' '),i[0])
        else:
            row = '         ' + numbers[0] +'         {} ⇒    {}\n'.format(i[1].ljust(15,' '),i[0])
        message_shedule += row
        message_shedule += '━━━━━━━━━━━━━━━━\n'
        numbers.pop(0)
    return config.message['shedule'].format(user_class, days[day_week], message_shedule)  


@bot.callback_query_handler(func=lambda call: True)
def load_chapters(call):
    data = json.loads(call.data)
    function_name = data['fn']

    cases = {
            'tt': get_tt,
            'ls': get_lessons,
            'oth': other_class,
            'ott': other_class_t
            }

    method = cases[function_name]
    parameter1 = data['p']
    method(parameter1,call)


def get_tt(parameter, call):
    if parameter == "40pn":
        bot.send_message(call.message.chat.id, config.timetable["40min_Monday"])
    elif parameter == "40":
        bot.send_message(call.message.chat.id, config.timetable["40min_Tue-Fri"])
    elif parameter == "35":
        bot.send_message(call.message.chat.id, config.timetable["35min"])
    elif parameter == "30":
        bot.send_message(call.message.chat.id, config.timetable["30min"])

def get_lessons(parameter, call):
    bot.send_message(call.message.chat.id, generate_shedule(int(parameter[0]),call.from_user.id), reply_markup=murkups.other_class(int(parameter[0])))

def other_class(parameter, call):
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Понедельник (след. неделя)']
    bot.send_message(call.message.chat.id, 'Выберите необходимый Вам класс ниже (Расписание на {})👇'.format(days[parameter]), reply_markup=murkups.other_class_talbe(parameter))

def other_class_t(parameter, call):
    day = parameter[0]
    class_name = parameter[1::]
    bot.send_message(call.message.chat.id, generate_shedule(day_week=int(day),class_name=class_name), reply_markup=murkups.other_class(int(parameter[0])))

if __name__ == "__main__":
    classes = get_classes()
    bot.polling()