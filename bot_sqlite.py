import telebot
import requests
import datetime
from database import Database

bot = telebot.TeleBot("8814124846:AAFCXv9uPAaDermMt0bYIsQVdZek950gbxA")

db = Database("bot.db")
db.create_tables()
bot = telebot.TeleBot("8814124846:AAFCXv9uPAaDermMt0bYIsQVdZek950gbxA")

db = Database("bot.db")
db.create_tables()
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    name = message.from_user.first_name
    db.add_user(user_id, name)
    bot.send_message(user_id, f"Привет, {name}! Я бот.")


@bot.message_handler(commands=["save"])
def save_note(message):
    user_id = message.chat.id
    note = message.text.replace("/save", "").strip()
    db.add_note(user_id, note)
    bot.send_message(user_id, "Записал: " + note)


@bot.message_handler(commands=["list"])
def list_notes(message):
    user_id = message.chat.id
    notes = db.get_notes(user_id)

    if notes:
        result = ""
        for i in range(len(notes)):
            result = result + f"{i+1}. {notes[i][0]}\n"
        bot.send_message(user_id, "Твои заметки:\n" + result)
    else:
        bot.send_message(user_id, "Заметок пока нет")


@bot.message_handler(commands=["del"])
def del_note(message):
    user_id = message.chat.id
    number = message.text.replace("/del", "").strip()

    if not number.isdigit():
        bot.send_message(user_id, "Напиши номер: /del 2")
        return

    index = int(number) - 1

    if db.delete_note(user_id, index):
        bot.send_message(user_id, "Удалил заметку " + number)
    else:
        bot.send_message(user_id, "Такой заметки нет")


@bot.message_handler(commands=["count"])
def count_notes(message):
    user_id = message.chat.id
    count = db.count_notes(user_id)
    bot.send_message(user_id, f"У тебя {count} заметок")


@bot.message_handler(commands=["clear"])
def clear_notes(message):
    user_id = message.chat.id
    db.clear_notes(user_id)
    bot.send_message(user_id, "Все заметки удалены")


@bot.message_handler(commands=["help"])
def help_command(message):
    text = (
        "Мои команды:\n"
        "/start — начать\n"
        "/save текст — сохранить заметку\n"
        "/list — показать заметки\n"
        "/del номер — удалить заметку\n"
        "/count — сколько заметок\n"
        "/clear — удалить все заметки\n"
        "\n"
        "А ещё я понимаю:\n"
        "привет, пока, погода, шутка, время"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True)
def answer(message):
    text = message.text.lower()
    if text == "привет":
        bot.send_message(message.chat.id, "Здравия желаю, товарищ!")
    elif text == "пока":
        bot.send_message(message.chat.id, "До связи")
    elif text == "погода":
        response = requests.get("https://wttr.in/Moscow?format=3")
        bot.send_message(message.chat.id, response.text)
    elif text == "время":
        now = datetime.datetime.now()
        bot.send_message(message.chat.id, now.strftime("%H:%M:%S"))
    elif text == "шутка":
        response = requests.get("https://api.chucknorris.io/jokes/random")
        data = response.json()
        bot.send_message(message.chat.id, data["value"])
    else:
        bot.send_message(message.chat.id, "Не понял")


bot.polling()

