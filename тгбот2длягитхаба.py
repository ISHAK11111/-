import telebot
import math
bot = telebot.TeleBot("Ишак")
@bot.message_handler(commands=['start'])
def start(m):
    t = "Привет! Я бот для расчета углов в линзе. Напиши 'считать' чтобы начать."
    bot.send_message(m.chat.id, t)
@bot.message_handler(commands=['calc'])
def calc(m):
    bot.send_message(m.chat.id, "Введи показатель преломления (n):")
    bot.register_next_step_handler(m, get_n)
@bot.message_handler(func=lambda m: True)
def all_msg(m):
    if m.text.lower() == 'считать':
        bot.send_message(m.chat.id, "Введи показатель преломления (n):")
        bot.register_next_step_handler(m, get_n)
    else:
        bot.send_message(m.chat.id, "Напиши 'считать' или используй /calc")
def get_n(m):
    n = m.text
    if n.replace('.','').isdigit():
        n=float(n)
        if n>1:
            bot.send_message(m.chat.id, f"n={n}. Теперь введи угол падения:")
            bot.register_next_step_handler(m, get_angle, n)
        else:
            bot.send_message(m.chat.id, "n должен быть больше 1. Напиши 'считать'")
    else:
        bot.send_message(m.chat.id, "Это не число. Напиши 'считать'")
def get_angle(m, n):
    a = m.text
    if a.replace('.','').isdigit():
        a =float(a)
        if 0<=a< 90:
            ar=math.radians(a)
            sa=math.sin(ar)
            sb=sa/ n
            if sb<=1:
                br=math.asin(sb)
                bd=math.degrees(br)
                bot.send_message(m.chat.id, f"Угол преломления: {bd:.1f}°")
            else:
                bot.send_message(m.chat.id, "Полное отражение!")
        else:
            bot.send_message(m.chat.id, "Угол от 0 до 90. Напиши 'считать'")
    else:
        bot.send_message(m.chat.id, "Это не число. Напиши 'считать'")
print("Бот работает...")
bot.polling()