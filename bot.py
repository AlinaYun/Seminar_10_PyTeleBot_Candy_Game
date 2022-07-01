import telebot
from telebot import types
import time
import random

# название бота @CandyGameTestBot

with open('Token.txt', 'r') as f:
    Token = f.read()

bot = telebot.TeleBot(Token)

total_number_of_candies = 100 #всего конфет
number_to_take = 28 # кол-во конфет, которые можно забрать за 1 ход


@bot.message_handler(commands=['start'])
def button(message):
    bot.send_message(message.chat.id, text=f"Привет! Предлагаю игру: на столе лежит {total_number_of_candies} конфет(а). За один ход можно забрать не более, чем {number_to_take} штук. Все конфеты оппонента достаются сделавшему последний ход.")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Хочешь сыграть? Для ответа нажми кнопку 'Да' или 'Нет'", reply_markup=markup )


@bot.message_handler(content_types=['text'])
def user_reply(message):
    global turn
    global total_number_of_candies
    if message.text == "Да":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton("Бросить кубик"))
        msg = bot.send_message(message.chat.id, text="Определим очередность хода. \nЧтобы бросить кубик, нажми кнопку 'Бросить кубик'")
        bot.register_next_step_handler(msg, roll_dice)
    if message.text == "Нет":
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, text='Заходи, если передумаешь. Пока!')



def roll_dice(message):
    global turn
    while True:
        playerl = bot.send_dice(message.chat.id,)
        time.sleep(4) # время на прокручивание кубиков
        bot.send_message(message.chat.id, text="Теперь бросаю я.")
        player2 = bot.send_dice(message.chat.id)
        time.sleep(4)   # время на прокручивание кубиков
        if playerl.dice.value > player2.dice.value:
            turn = 1
            break
        elif playerl.dice.value < player2.dice.value:
            bot.send_message(message.chat.id, text="Я хожу первым")
            turn = 2
            break
        else: 
            bot.send_message(message.chat.id, text="Ничья. Бросаем еще раз.")
    game(message)
    

        

def game (message):
    global total_number_of_candies
    global turn
    if total_number_of_candies > number_to_take:
        if turn == 1:
            msg = bot.send_message(message.chat.id, f"Твой ход: сколько конфет берешь? (введи число от 1 до {number_to_take})")
            bot.register_next_step_handler(msg, user_input)
        if turn == 2:
            bot_take = random.randint(1,number_to_take+1)
            total_number_of_candies -= bot_take
            bot.send_message(message.chat.id, text=f"Мой ход: я беру {bot_take} конфет(у/ы). Осталось *{total_number_of_candies}*", parse_mode="Markdown")
            turn = 1
            game(message)
    else:
        if turn == 1:
            stic = open('sticker.webp', 'rb')
            bot.send_message(message.chat.id, text=f"Ты забираешь оставшиеся конфеты. Ты выйграл!")
            bot.send_sticker(message.chat.id, stic)
        if turn == 2:
            bot.send_message(message.chat.id, text=f"Я забираю оставшиеся {total_number_of_candies}. Я выйграл!")

    
def user_input(message):
    global total_number_of_candies
    global turn
    if int(message.text.isdigit()) and 0 < int(message.text) <= number_to_take:
        total_number_of_candies -= int(message.text)
        bot.send_message(message.chat.id, text=f"Осталось *{total_number_of_candies}* конфет", parse_mode="Markdown")
        turn = 2
    else:
        bot.send_message(message.chat.id, text="Введено некорректное значение. Нужно ввести число от 1 до 28")
    game(message)




    

        




bot.polling(none_stop=True)