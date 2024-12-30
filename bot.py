import telebot
from telebot import types
import time
import tkinter
from tkinter import *
from threading import Thread
import os

# не забывай востанавливать прогу! файл backup.txt в помощь


def clicked():
    global command_panel
    command_panel = entry_obj.get()
    admin_panel(command_panel)

def admin_panel(com):
    if com == "taps":
        os.system('cls')
        print(taps)
    elif com == "members":
        os.system('cls')
        print(taps.keys())
    elif com == "taps.correct":
        user = int(input("Айди - "))
        tapers = int(input("Число тапов - "))
        if tapers < 0:
            taps[user] -= tapers
        else:
            taps[user] += tapers
    else:
        try:
            eval(com)
        except:
            os.system('cls')
            print("error")

taps = {}
refers1 = {}
refers2 = {}
referals = []
command_panel = ""

buster_tap = {} # id : lvl of buster
maining_buster_tap = {0: 0, 1: 0.2, 2: 0.5, 3: 1, 4: 1.2, 5: 1.5, 6: 2, 7: 2.2, 8: 2.5, 9: 3, 10: 9.2}

passive = {} # id : lvl of passive

buster_passive = {} # id : lvl of buster

buying_item = ""

panel = Tk()
panel.title("Telebot Admin Panel")
panel.resizable(False, False)
panel.geometry("500x300")
p_btn = Button(panel, text="OK", background = "grey", activebackground = "lightgrey", command = clicked)
p_btn.place(x = 200, y = 200, width = 100, height = 50)
entry_obj = Entry(panel, width = 70)
entry_obj.place(x = 25, y = 100)

token = "токен"
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ["hello"])
def hello_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)
    bot.reply_to(mess, "Привет", reply_markup = markup)

@bot.message_handler(commands = ["start"])
def start_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Режим тапинга")
    btn2 = types.KeyboardButton("Поздороваться")
    markup.add(btn1, btn2)
    bot.reply_to(mess, "Привет! Ты попал в Тапателя - подобия хомяка, но более выгодного! Скорей начинай тапать по команде /taping или нажав на кнопку \"Режим тапинга\"", reply_markup = markup)
    #     bot.send_audio(mess.chat.id, audio = open("photo_2024-12-08_12-56-08.jpg", "rb"))

@bot.message_handler(commands = ["taping"])
def taping_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тапнуть")
    btn2 = types.KeyboardButton("Баланс")
    btn3 = types.KeyboardButton("Назад")
    btn4 = types.KeyboardButton("Стать рефером")
    btn5 = types.KeyboardButton("Стать рефералом")
    btn6 = types.KeyboardButton("Топ по тапам")
    btn7 = types.KeyboardButton("Пассив и бустеры")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.reply_to(mess, "Начинай тапать! Что бы тапнуть, введи /tap, а что бы узнать баланс, напиши /bal", reply_markup = markup)
    if mess.chat.id not in taps:
        taps[mess.chat.id] = 0
        print(mess.chat.id)
    if mess.chat.id not in buster_tap:
        buster_tap[mess.chat.id] = 0

@bot.message_handler(commands = ["bal"])
def balance_dialoge(mess):
    if mess.chat.id not in taps:
        taps[mess.chat.id] = 0
        print(mess.chat.id)
    bot.reply_to(mess, f"Твой баланс - {int(taps[mess.chat.id])}")

@bot.message_handler(commands = ["tap"])
def tap_dialoge(mess):
    global taps
    bot.send_message(mess.chat.id, ".")
    if mess.chat.id not in taps:
        taps[mess.chat.id] = 0
        print(mess.chat.id)
    if mess.chat.id in refers2:
        taps[refers2[mess.chat.id]] += 0.1
    taps[mess.chat.id] += maining_buster_tap[buster_tap[mess.chat.id]]
    taps[mess.chat.id] = taps[mess.chat.id] + 1

@bot.message_handler(commands = ["refer"])
def refer_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Режим тапинга")
    markup.add(btn1)
    bot.reply_to(mess, f"Хочешь стать рефером? Окей! Твой id надо будет сообщить другу. Вот он - {mess.chat.id}", reply_markup = markup)
    refers1[mess.chat.id] = []

@bot.message_handler(commands = ["referal"])
def referal_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Режим тапинга")
    markup.add(btn1)
    bot.reply_to(mess, f"Хочешь стать рефералом? Окей! Тебе надо сказать ID своего рефера. Он должен был тебе его сообщить", reply_markup = markup)
    bot.register_next_step_handler(mess, referalsss)

@bot.message_handler(commands = ["top"])
def top_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Режим тапинга")
    markup.add(btn1)
    topers = dict(sorted(taps.items(), key=lambda item: item[1], reverse=True))
    text_to_share = "Вот список лидеров:"
    toperss = 0
    for key, value in topers.items():
        if toperss == 3:
            break
        toperss += 1
        text_to_share += "\n{0} -> {1} тапов".format(key, int(value))
    bot.reply_to(mess, text_to_share, reply_markup = markup)


@bot.message_handler(commands = ["buster_tap"])
def buster_tap_dialoge(mess):
    global buying_item
    if mess.chat.id not in buster_tap:
        buster_tap[mess.chat.id] = 0
    if buster_tap[mess.chat.id] < 10:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        buying_item = "buster_tap"
        bot.reply_to(mess, f"Ваш уровень бустера тапа - {buster_tap[mess.chat.id]}. Прокачать до {buster_tap[mess.chat.id] + 1} уровня за {(buster_tap[mess.chat.id] + 1) * 100} тапов?", reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Режим тапинга")
        markup.add(btn1)
        bot.reply_to(mess, "У вас максимальный уровень!", reply_markup = markup)

@bot.message_handler(commands = ["passive_busters"])
def passive_busters_dialoge(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton("Пассив")
    btn2 = types.KeyboardButton("Бустер тапа")
    btn3 = types.KeyboardButton("Бустер пассива")
    markup.add(btn1, btn2, btn3)
    bot.reply_to(mess, "Что вы хотите приобрести?", reply_markup = markup)

@bot.message_handler(comands = ["passive"])
def passive_dialoge(mess):
    global buying_item
    if mess.chat.id not in passive:
        passive[mess.chat.id] = 0
    if passive[mess.chat.id] < 100:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        buying_item = "passive"
        bot.reply_to(mess, f"Ваш уровень пассива - {passive[mess.chat.id]}. Прокачать до {passive[mess.chat.id] + 1} уровня за {(passive[mess.chat.id] + 1) * 100} тапов?", reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Режим тапинга")
        markup.add(btn1)
        bot.reply_to(mess, "У вас максимальный уровень!", reply_markup = markup)

@bot.message_handler(comands = ["buster_passive"])
def buster_passive_dialoge(mess):
    global buying_item
    if mess.chat.id not in buster_passive:
        buster_passive[mess.chat.id] = 0
    if buster_passive[mess.chat.id] < 20:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        buying_item = "buster_passive"
        bot.reply_to(mess, f"Ваш уровень бустера пассива - {buster_passive[mess.chat.id]}. Прокачать до {buster_passive[mess.chat.id] + 1} уровня за {(buster_passive[mess.chat.id] + 1) * 100} тапов?", reply_markup = markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Режим тапинга")
        markup.add(btn1)
        bot.reply_to(mess, "У вас максимальный уровень!", reply_markup = markup)
    
def buying(mess, type_of_buy):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Режим тапинга")
    markup.add(btn1)
    
    if type_of_buy == "buster_tap":
        if taps[mess.chat.id] >= (buster_tap[mess.chat.id] + 1) * 100:
            taps[mess.chat.id] -= (buster_tap[mess.chat.id] + 1) * 100
            buster_tap[mess.chat.id] += 1
            bot.reply_to(mess, "Вы оплатили новый уровень!", reply_markup = markup)
        else:
            bot.reply_to(mess, f"У вас недостаточно тапов! Надо еще {(buster_tap[mess.chat.id] + 1) * 100 - taps[mess.chat.id]} тапа(ов)", reply_markup = markup)
            
    elif type_of_buy == "passive":
        if taps[mess.chat.id] >= (passive[mess.chat.id] + 1) * 200:
            taps[mess.chat.id] -= (passive[mess.chat.id] + 1) * 200
            passive[mess.chat.id] += 1
            bot.reply_to(mess, "Вы оплатили новый уровень!", reply_markup = markup)
        else:
            bot.reply_to(mess, f"У вас недостаточно тапов! Надо еще {(passive[mess.chat.id] + 1) * 100 - taps[mess.chat.id]} тапа(ов)", reply_markup = markup)

    elif type_of_buy == "buster_passive":
        if taps[mess.chat.id] >= (buster_passive[mess.chat.id] + 1) * 200:
            taps[mess.chat.id] -= (buster_passive[mess.chat.id] + 1) * 200
            buster_passive[mess.chat.id] += 1
            bot.reply_to(mess, "Вы оплатили новый уровень!", reply_markup = markup)
        else:
            bot.reply_to(mess, f"У вас недостаточно тапов! Надо еще {(buster_passive[mess.chat.id] + 1) * 100 - taps[mess.chat.id]} тапа(ов)", reply_markup = markup)

def adding_referal(msg):
    refers1[int(msg.text)].append(msg.chat.id)
    refers2[msg.chat.id] = int(msg.text)
    referals.append(msg.chat.id)
    bot.send_message(refers2[msg.chat.id], f"Опана. У тебя новый реферал - @{msg.chat.username} (если выводится @None, то это значит что у твоего реферала нет никнейма)")

@bot.message_handler(content_types=['text'])
def buttons(mess):
    global buying_item
    
    if mess.text == "Режим тапинга" or mess.text == "Нет":
        taping_dialoge(mess)
    elif mess.text == "Поздороваться":
        sendMessage(mess)
    elif mess.text == "Тапнуть":
        tap_dialoge(mess)
    elif mess.text == "Баланс":
        balance_dialoge(mess)
    elif mess.text == "Назад":
        start_dialoge(mess)
    elif mess.text == "Стать рефером":
        refer_dialoge(mess)
    elif mess.text == "Стать рефералом":
        referal_dialoge(mess)
    elif mess.text == "Топ по тапам":
        top_dialoge(mess)
    elif mess.text == "Да":
        buying(mess, buying_item)
    elif mess.text == "Пассив и бустеры":
        passive_busters_dialoge(mess)
    elif mess.text == "Бустер тапа":
        buster_tap_dialoge(mess)
    elif mess.text == "Пассив":
        passive_dialoge(mess)
    elif mess.text == "Бустер пассива":
        start_dialoge1(mess)
    else:
        bot.reply_to(mess, "Скажи прогерам @tapatel_help_bot что на такое я не запрограммирован")

potok = Thread(target = bot.infinity_polling)
potok.start()
panel.mainloop()
