import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from backend import Employee, Subject, Test, Statistics, User
from config import BOT_TOKEN
from datetime import date as sana
import sqlite3


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def action(update, context):
    context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)


ADMIN = '590924106'#'561859007'#'959798930'
# employee_object = Employee()

admin_states = {
    'start': 'a1',
    'menyu': 'a2',

    'hodimlar': 'a3.1',
    'hodim_ismi': 'a3.2',
    'hodim_ishjoyi': 'a3.3',
    'hodim_lavozimi': 'a3.4',
    'hodim_paroli': 'a3.5',
    
    'fanlar1': 'a4.1',
    'fanlar2': 'a4.2',
    'fanlar3': 'a4.3',

    'testlar': 'a5.1',
    'testlar1': 'a5.1',
    'testlar2': 'a5.2',
    'testlar3': 'a5.3',
    'test_a': 'a5.4',
    'test_b': 'a5.5',
    'test_c': 'a5.6',
    'test_d': 'a5.7',

    'statistika': 'a6.1',
    'statistika_subject': 'a6.2',
    'statistika_employee': 'a6.3',
}

user_states = {
    'start': 'u1',

    'menyu': 'u2',

    'test': 'u3'

}

# Variables for use in future
admin_steps = {}
test_steps = {}

def start(update, context):
    chat_id = str(update.message.from_user.id)
    print(chat_id)
    if chat_id == ADMIN:
        update.message.reply_text("Aссалому алейкум. Менюлардан бирини танланг:", reply_markup=admin_menyu)
        return admin_states['start']
    else:
        update.message.reply_text("Фойдаланиш учун шахсий паролингизни киритинг!", reply_markup=ReplyKeyboardRemove())
        return user_states['start']


def backTomenyu(update, context):
    update.message.reply_text("Aсосий менюга қайтдингиз:", reply_markup=admin_menyu)
    return admin_states['start']


def employees(update, context):
    employee_object = Employee()
    hodimlar = employee_object.select_employees()
    if not hodimlar:
        update.message.reply_text("Сизда ҳодимлар мавжуд эмас! Янги ҳодим қўшишингиз мумкин.", reply_markup=ReplyKeyboardMarkup([
            ["Янги ҳодим қўшиш"], ["Орқага"]
        ], resize_keyboard=True))
    else:
        update.message.reply_text("Сизнинг ҳодимларингиз:", reply_markup=ReplyKeyboardMarkup([
            ["Янги ҳодим қўшиш"], ["Орқага"]
        ], resize_keyboard=True))
        for hodim in hodimlar:
            employee_data = "Ҳодим: " + hodim[1] + ' ' + hodim[2] + '\nИш жойи: ' + hodim[3] + '\nЛавозими: ' \
                            + hodim[4] + '\nПарол: ' + hodim[5]
            update.message.reply_text(employee_data, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Ўчириш', callback_data=hodim[0])]
            ]))
    return admin_states['hodimlar']


def delete_employee(update, context):
    callback = update.callback_query
    employee_object = Employee()
    employee_object.delete_employee(callback.data)
    callback.edit_message_text("Ҳодим ўчирилди!")


def new_employee(update, context):
    admin_steps.update({'new_employee': dict()})
    update.message.reply_text("Янги ҳодимнинг исм ва фамилиясини киритинг.", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return admin_states['hodim_ismi']


def employee_name(update, context):
    name = update.message.text
    if name.count(' ') == 1:
        name = name.split()
        if name[0].isalpha() and name[1].isalpha():
            admin_steps['new_employee']['name'] = name[0]
            admin_steps['new_employee']['surname'] = name[1]
            update.message.reply_text("Ҳодимнинг иш жойини киритинг.")
            return admin_states['hodim_ishjoyi']
        else:
            update.message.reply_text("Илтимос исм ва фамилияни тўғри киритинг!")
    else:
        update.message.reply_text("Илтимос исм ва фамилияни тўғри киритинг!")


def employee_address(update, context):
    admin_steps['new_employee']['address'] = update.message.text
    update.message.reply_text("Ҳодимнинг лавозимини киритинг.")
    return admin_states['hodim_lavozimi']


def employee_degree(update, context):
    admin_steps['new_employee']['degree'] = update.message.text
    update.message.reply_text("Ҳодимнинг такрорланмас паролини киритинг.")
    return admin_states['hodim_paroli']


def employee_password(update, context):
    admin_steps['new_employee']['password'] = update.message.text
    a = admin_steps['new_employee']
    employee_object = Employee()
    try:
        employee_object.insert_employee(a['name'], a['surname'], a['address'], a['degree'], a['password'])
        del admin_steps['new_employee']
        update.message.reply_text("Маълумотлар сақланди. Aсосий меню:", reply_markup=admin_menyu)
    except Exception as e:
        print(str(e))
        update.message.reply_text("Парол такрор киритилди! Маълумотлар сақланмади.", reply_markup=admin_menyu)
    return admin_states['start']


def subjects(update, context):
    subjects_object = Subject()
    fanlar = subjects_object.select_subjects()
    if not fanlar:
        update.message.reply_text("Сизда фанлар мавжуд эмас! Янги фан қўшишингиз мумкин.",
                                  reply_markup=ReplyKeyboardMarkup([
                                      ["Янги фан қўшиш"], ["Орқага"]
                                  ], resize_keyboard=True))
    else:
        update.message.reply_text("Сизнинг фанларингиз:", reply_markup=ReplyKeyboardMarkup([
            ["Янги фан қўшиш"], ["Орқага"]
        ], resize_keyboard=True))
        keyboard = []
        for fan in fanlar:
            keyboard.append([InlineKeyboardButton(fan[1] + " ❌", callback_data=fan[0])])
        update.message.reply_text("Янги фан қўшиш ёки фанларни ўчиришингиз мумкин.", reply_markup=InlineKeyboardMarkup(keyboard))
    return admin_states['fanlar1']


def delete_subject(update, context):
    callback = update.callback_query
    subject_object = Subject()
    subject_object.delete_subject(callback.data)
    fanlar = subject_object.select_subjects()
    if not fanlar:
        callback.message.reply_text("Сизда фанлар мавжуд эмас! Янги фан қўшишингиз мумкин.")
    else:
        callback.edit_message_text("Фaн ўчирилди!")
        keyboard = []
        for fan in fanlar:
            keyboard.append([InlineKeyboardButton(fan[1] + " ❌", callback_data=fan[0])])
        callback.message.reply_text("Сизнинг фанларингиз:", reply_markup=InlineKeyboardMarkup(keyboard))


def new_subject(update, context):
    update.message.reply_text("Янги фан номини киритинг.", reply_markup=ReplyKeyboardMarkup([
        ["Орқага"]
    ], resize_keyboard=True))
    return admin_states['fanlar2']


def add_subject(update, context):
    subject_name = update.message.text
    subject_object = Subject()
    subject_object.insert_subject(subject_name)
    update.message.reply_text("Янги фан сақланди.", reply_markup=admin_menyu)
    return admin_states['start']


def tests(update, context):
    subject_object = Subject()
    fanlar = subject_object.select_subjects()
    keyboard = []
    update.message.reply_text("Фанлар:", reply_markup=ReplyKeyboardMarkup([
        ['Орқага']
    ], resize_keyboard=True))
    for fan in fanlar:
        keyboard.append([InlineKeyboardButton(fan[1], callback_data=fan[0])])
    update.message.reply_text("Фанлардан бирини танланг.", reply_markup=InlineKeyboardMarkup(keyboard))
    return admin_states['testlar1']


def test_fan(update, context):
    callback = update.callback_query
    test_object = Test()
    admin_steps['testForSubject'] = callback.data
    testlar = test_object.select_tests(callback.data)
    if not testlar:
        callback.message.delete()
        callback.message.reply_text("Бу фанда тестлар мавжуд эмас.", reply_markup=ReplyKeyboardMarkup([
            ["Янги тест қўшиш"], ['Орқага']
        ], resize_keyboard=True))
    else:
        callback.message.delete()
        callback.message.reply_text("Тестлар:", reply_markup=ReplyKeyboardMarkup([
            ["Янги тест қўшиш"], ['Орқага']
        ], resize_keyboard=True))
        for i in range(len(testlar)):
            text = str(i + 1) + ". " + testlar[i]['question'] + "\nA) " + testlar[i]['a'] + "\nB) " + testlar[i]['b'] \
                   + "\nC) " + testlar[i]['c'] + "\nD) " + testlar[i]['d']
            callback.message.reply_text(text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Ўчириш", callback_data=testlar[i]['test_id'])]]))
    return admin_states['testlar2']


def delete_test(update, context):
    callback = update.callback_query
    test_object = Test()
    test_object.delete_test(callback.data)
    callback.edit_message_text("Тест ўчирилди.")


def new_test(update, context):
    update.message.reply_text("Янги тестнинг саволини киритинг.", reply_markup=ReplyKeyboardMarkup([
        ["Орқага"]
    ], resize_keyboard=True))
    admin_steps.update({'new_test': dict()})
    return admin_states['testlar3']


def test_question(update, context):
    admin_steps['new_test']['question'] = update.message.text
    update.message.reply_text("Тестнинг A жавобини киритинг.")
    return admin_states['test_a']


def test_answer_a(update,context):
    admin_steps['new_test']['a'] = update.message.text
    update.message.reply_text("Тестнинг Б жавобини киритинг.")
    return admin_states['test_b']


def test_answer_b(update,context):
    admin_steps['new_test']['b'] = update.message.text
    update.message.reply_text("Тестнинг C жавобини киритинг.")
    return admin_states['test_c']


def test_answer_c(update,context):
    admin_steps['new_test']['c'] = update.message.text
    update.message.reply_text("Тестнинг Д жавобини киритинг.")
    return admin_states['test_d']


def test_answer_d(update,context):
    admin_steps['new_test']['d'] = update.message.text
    a = admin_steps['new_test']
    test_object = Test()
    test_object.insert_test(a['question'], a['a'], a['b'], a['c'], a['d'], admin_steps['testForSubject'])
    update.message.reply_text("Янги тест сақланди.", reply_markup=admin_menyu)
    return admin_states['start']


def statistics(update, context):
    update.message.reply_text("Менюлардан бирини танланг:", reply_markup=ReplyKeyboardMarkup([
        ["Фанлар", "Даражалар"], ["Орқага"]
    ], resize_keyboard=True))
    return admin_states['statistika']


def statistic_subject(update, context):
    keyboard = subject_buttons()
    update.message.reply_text("Фанлардан бирини танланг.", reply_markup=ReplyKeyboardMarkup([
        ["Орқага"]
    ], resize_keyboard=True))
    update.message.reply_text("Фанлар:", reply_markup=InlineKeyboardMarkup(keyboard))
    return admin_states['statistika_subject']


def subject_callback(update, context):
    callback = update.callback_query
    statistic_object = Statistics()
    results = statistic_object.join_employee_subject(callback.data)
    callback.message.delete()
    callback.message.reply_text("Тест натижалари: ", reply_markup=ReplyKeyboardMarkup([
        ["Орқага"]
    ], resize_keyboard=True))
    for result in results:
        text = "Ҳодим: " + result[1] + ' ' + result[2] + '\nИш жойи: ' + result[3] + '\nЛавозими: ' + result[4] \
               + "\nУмумий саволлар сони: " + str(result[9]) + "\nТўғри жавоблар сони: " + str(result[10]) + "\nТест санаси: " + str(result[11])
        callback.message.reply_text(text)

    return admin_states['statistika']


def statistic_degree(update, context):
    keyboard = degree_buttons()
    update.message.reply_text("Лавозимлардан бирини танланг.")
    update.message.reply_text("Лавозимлар:", reply_markup=InlineKeyboardMarkup(keyboard))
    return admin_states['statistika_employee']


def degree_callback(update, context):
    callback = update.callback_query
    statistic_object = Statistics()
    results = statistic_object.join_employee_position(callback.data)
    callback.message.delete()
    callback.message.reply_text("Тест натижалари: ", reply_markup=ReplyKeyboardMarkup([
        ["Орқага"]
    ], resize_keyboard=True))
    for result in results:
        text = "Ҳодим: " + result[1] + ' ' + result[2] + '\nИш жойи: ' + result[3] + '\nЛавозими: ' + result[4] \
               + "\nУмумий саволлар сони: " + str(result[9]) + "\nТўғри жавоблар сони: " + str(result[10]) \
               + "\nТест санаси: " + str(result[11]) + "\nТест топширилган фан: " + result[13]
        callback.message.reply_text(text)

    return admin_states['statistika']


def degree_buttons():
    employee_object = Employee()
    degrees = employee_object.select_position()
    keyboard = []
    keys = []
    for degree in degrees:
        keys.append(InlineKeyboardButton(degree[0], callback_data=degree[0]))
        if len(keys) == 2:
            keyboard.append(keys)
            keys = []
        if degree == degrees[-1]:
            if len(degrees) % 2 == 1:
                keyboard.append([InlineKeyboardButton(degree[0], callback_data=degree[0])])
    return keyboard


def subject_buttons():
    subject_object = Subject()
    fanlar = subject_object.select_subjects()
    keyboard = []
    keys = []
    for fan in fanlar:
        keys.append(InlineKeyboardButton(fan[1], callback_data=fan[0]))
        if len(keys) == 2:
            keyboard.append(keys)
            keys = []
        if fan == fanlar[-1]:
            if len(fanlar) % 2 == 1:
                keyboard.append([InlineKeyboardButton(fan[1], callback_data=fan[0])])
    return keyboard

def check_password(update, context):
    password = update.message.text
    chat_id = str(update.message.from_user.id)
    employee_object = User()
    keyboard = subject_buttons()
    result = employee_object.check_password(password)
    if result[0]:
        test_steps.update({
            chat_id: {'id': str(result[1][0])}
        })
        text = "Тест ботига хуш келибсиз. Тест ишлаш учун фанлардан бирини танланг:"
        update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return user_states['menyu']
    else:
        update.message.reply_text("Парол хато киритилди!")


def show_subject_test(update, context):
    test_object = Test()
    callback = update.callback_query
    chat_id = str(callback.from_user.id)
    callback.message.delete()
    test_steps[chat_id]['subject'] = callback.data
    testlar = test_object.select_tests(callback.data)
    callback.message.reply_text("Тест саволлари:", reply_markup=ReplyKeyboardMarkup([
        ['Тугатиш']
    ], resize_keyboard=True))

    for i, test in enumerate(testlar):
        answers = {
            'A': '0',
            'B': '0',
            'C': '0',
            'D': '0',
        }
        array = [test[2], test[3], test[4], test[5]]
        random.shuffle(array)
        answer = array.index(test[2])
        answers[list(answers)[answer]] = '1'
        text = str(i + 1) +  '. ' + test[1] + '\nA)' + array[0] + '\nB)' + array[1] + '\nC)' + array[2] + '\nD)' + array[3]
        callback.message.reply_text(text, reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('A', callback_data=answers['A'] + 'A'),
                InlineKeyboardButton('B', callback_data=answers['B'] + 'B'),
                InlineKeyboardButton('C', callback_data=answers['C'] + 'C'),
                InlineKeyboardButton('D', callback_data=answers['D'] + 'D')
            ]
        ]))

    test_steps[chat_id].update({
        'start_test': callback.message.message_id + 2,
        'count_test': len(testlar),
        'answers': 0
    })
    return user_states['test']

def check_test(update, context):
    callback = update.callback_query
    chat_id = str(callback.from_user.id)
    if callback.data[0] == '1':
        test_steps[chat_id]['answers'] += 1
        callback.edit_message_text("Тест тўғри ечилди ✅.")
    else:
        inlines = callback.message['reply_markup']['inline_keyboard'][0]
        true_ans = 'x'
        for inline in inlines:
            if inline['callback_data'][0] == '1':
                true_ans = inline['callback_data'][1]
        answers = callback.message.text.split('\n')
        for answer in answers:
            if answer[0] == true_ans:
                callback.edit_message_text("Тест хато ечилди ❌.\nТўғри жавоб: " + answer)


def end_test(update, context):
    chat_id = str(update.message.from_user.id)
    for message_id in range(test_steps[chat_id]['count_test']):
        context.bot.delete_message(chat_id, message_id + test_steps[chat_id]['start_test'])

    text = "Сиз хозир " + str(test_steps[chat_id]['count_test']) + " та тестдан " + str(test_steps[chat_id]['answers']) + " тасини тўғри ечдингиз."
    update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    statistics_object = Statistics()
    date = sana.today().strftime("%d.%m.%Y")
    statistics_object.insert_statistics(test_steps[chat_id]['id'], test_steps[chat_id]['subject'],
                                        str(test_steps[chat_id]['count_test']), str(test_steps[chat_id]['answers']), date)
    keyboard = subject_buttons()
    update.message.reply_text("Aсосий менюга қайтдингиз:", reply_markup=InlineKeyboardMarkup(keyboard))
    return user_states['menyu']


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher


    controller = ConversationHandler(
        entry_points=[
            CommandHandler('start', start)
        ],
        states={
            admin_states['start']: [
                MessageHandler(Filters.regex('Ҳодимлар'), employees),
                MessageHandler(Filters.regex('Фанлар'), subjects),
                MessageHandler(Filters.regex('Тестлар'), tests),
                MessageHandler(Filters.regex('Статистика'), statistics)
            ],
            admin_states['hodimlar']: [
                CallbackQueryHandler(delete_employee),
                MessageHandler(Filters.regex("Янги ҳодим қўшиш"), new_employee),
                MessageHandler(Filters.regex("Орқага"), backTomenyu)
            ],
            admin_states['hodim_ismi']: [
                MessageHandler(Filters.text, employee_name)
            ],
            admin_states['hodim_ishjoyi']: [
                MessageHandler(Filters.text, employee_address)
            ],
            admin_states['hodim_lavozimi']: [
                MessageHandler(Filters.text, employee_degree)
            ],
            admin_states['hodim_paroli']: [
                MessageHandler(Filters.text, employee_password)
            ],
            admin_states['fanlar1']: [
                CallbackQueryHandler(delete_subject),
                MessageHandler(Filters.regex("Янги фан қўшиш"), new_subject),
                MessageHandler(Filters.regex('Орқага'), backTomenyu)
            ],
            admin_states['fanlar2']: [
                MessageHandler(Filters.text, add_subject)
            ],
            admin_states['testlar1']: [
                CallbackQueryHandler(test_fan),
                MessageHandler(Filters.regex('Орқага'), backTomenyu)
            ],
            admin_states['testlar2']: [
                CallbackQueryHandler(delete_test),
                MessageHandler(Filters.regex('Янги тест қўшиш'), new_test),
                MessageHandler(Filters.regex('Орқага'), backTomenyu)
            ],
            admin_states['testlar3']: [
                MessageHandler(Filters.regex('Орқага'), backTomenyu),
                MessageHandler(Filters.text, test_question)
            ],
            admin_states['test_a']: [
                MessageHandler(Filters.regex('Орқага'), backTomenyu),
                MessageHandler(Filters.text, test_answer_a)
            ],
            admin_states['test_b']: [
                MessageHandler(Filters.regex('Орқага'), backTomenyu),
                MessageHandler(Filters.text, test_answer_b)
            ],
            admin_states['test_c']: [
                MessageHandler(Filters.regex('Орқага'), backTomenyu),
                MessageHandler(Filters.text, test_answer_c)
            ],
            admin_states['test_d']: [
                MessageHandler(Filters.regex('Орқага'), backTomenyu),
                MessageHandler(Filters.text, test_answer_d)
            ],
            admin_states['statistika']: [
                MessageHandler(Filters.regex("Фанлар"), statistic_subject),
                MessageHandler(Filters.regex("Даражалар"), statistic_degree),
                MessageHandler(Filters.regex("Орқага"), backTomenyu)
            ],
            admin_states['statistika_subject']: [
                CallbackQueryHandler(subject_callback),
                MessageHandler(Filters.regex("Орқага"), backTomenyu)
            ],
            admin_states['statistika_employee']: [
                CallbackQueryHandler(degree_callback)
            ],
            user_states['start']: [
                MessageHandler(Filters.text, check_password)
            ],
            user_states['menyu']: [
                CallbackQueryHandler(show_subject_test)
            ],
            user_states['test']: [
                CallbackQueryHandler(check_test),
                MessageHandler(Filters.regex("Тугатиш"), end_test)
            ]
        },
        fallbacks=[
            CommandHandler('start', start),
        ]
    )

    dispatcher.add_handler(controller)
    dispatcher.add_handler(MessageHandler(Filters.text, action))
    updater.start_polling()
    updater.idle()


admin_menyu = ReplyKeyboardMarkup([
    ['Ҳодимлар'], ['Фанлар', 'Тестлар'], ['Статистика']
], resize_keyboard=True)



if __name__ == '__main__':
    main()
