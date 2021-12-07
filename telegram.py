import telebot
from telebot import types
import sqlite3 as lite
import time

client  = telebot.TeleBot('5072105165:AAHC1gODrStip9TfKbmNZK_EgUIsEm17xcs')


def message_step1(mes):
    sqlite_connection = lite.connect('db.sqlite3')
    with sqlite_connection:
        cursor = sqlite_connection.cursor()
        print("База данных успешно подключена к SQLite") 
        number = "0"
        price = "NUN"
        for row in cursor.execute('SELECT * FROM main_order'):
            if str(mes.chat.id) == str(row[6]): 
                number = str(row[0])
                price = str(row[3])
    
    markup_inline = types.InlineKeyboardMarkup()
    item3 = types.InlineKeyboardButton(text = '☆', callback_data = '3')
    item4 = types.InlineKeyboardButton(text = '☆☆', callback_data = '4')
    item5 = types.InlineKeyboardButton(text = '☆☆☆', callback_data = '5')
    item6 = types.InlineKeyboardButton(text = '☆☆☆☆', callback_data = '6')
    item7 = types.InlineKeyboardButton(text = '☆☆☆☆☆', callback_data = '7')
    markup_inline.add(item3,item4,item5,item6,item7)
    client.send_message(mes.chat.id,'Замовлення №'+number+' > Готовий \nДо сплати: '+price+'₴\nМелітополь, Запорізька область, Украина, 72300')
    client.send_message(mes.chat.id,'Дякуємо за замовлення!\nВам все сподобалось по замовленню №'+number+'?')
    client.send_message(mes.chat.id,'Оцініть якщо не складно)',reply_markup=markup_inline)
    
#start
@client.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Меню')
    markup.add(item1)
    number = message.text.split()[-1] #разбить на слова и выбрать последнее
    print("Номер заказа: "+ str(number)) #id заказа
    
    sqlite_connection = lite.connect('db.sqlite3')
    with sqlite_connection:
        cursor = sqlite_connection.cursor()
        print("База данных успешно подключена к SQLite")
        cursor.execute("UPDATE main_order SET IdTelegram='"+str(message.chat.id)+"' WHERE id="+str(number))
                
        price = "0"
        name = ""
        for row in cursor.execute('SELECT * FROM main_order'):
            if str(row[0]) == str(number): 
                name = ", " + str(row[1])
                price = str(row[3])
    
    # cursor.close()
    client.send_message(message.chat.id, ('Доброго дня'+ name+'.\n\nВаш номер замовлення ' + str(number) + '.\nДо сплати '+price+'₴\n\nМи Вас повідомимо, коли замовлення буде готове!'), reply_markup = markup)
    time.sleep(10)
    message_step1(message)
    

#Menu
@client.message_handler(content_types = ['text'])
def bot_menu(message):
    if message.chat.type=='private':
        if message.text=='Меню':
            markup_inline = types.InlineKeyboardMarkup()
            item2 = types.InlineKeyboardButton(text = 'Ссылка', callback_data = '2')
            markup_inline.add(item2)
            client.send_message(message.chat.id, 'Натисніть кнопку, щоб перейти у меню', reply_markup = markup_inline)

        elif message.text=='1':
           message_step1(message)

@client.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.message:
        if call.data =='3':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'Дякую, ви оцінили на 1.')
        elif call.data =='4':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'Дякую, ви оцінили на 2.')
        elif call.data =='5':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'Дякую, ви оцінили на 3.')
        elif call.data =='6':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'Дякую, ви оцінили на 4.')
        elif call.data =='7':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'Дякую, ви оцінили на 5.')
        elif call.data =='2':
            client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,text= 'http://127.0.0.1:8000/')


#client.polling(none_stop=True, interval=0)
client.polling(interval=0)