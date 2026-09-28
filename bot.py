import telebot
import requests
import json
import os
import datetime

bot = telebot.TeleBot("Токен_бота")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,"Привет! Я бот.")
@bot.message_handler(commands=["save"])
def save_note(message):
    note = message.text.replace("/save", " ").strip()
    if os.path.exists("notes.json"):
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    else:
        notes = []
    notes.append(note)
    with open("notes.json", "w", encoding="utf-8") as file:
           json.dump(notes, file, ensure_ascii=False)
    bot.send_message(message.chat.id, "записал " + note)
           
@bot.message_handler(commands=["list"])
def list_notes(message):
    if os.path.exists("notes.json"):
        with open("notes.json", "r" , encoding="utf-8")as file:
            notes = json.load(file)
        result = " "
        for i in range(len(notes)):
               result = result + f"{i+1}. {notes[i]}\n"
        bot.send_message(message.chat.id, "твои заметки:\n" +result)
    else:
            bot.send_message(message.chat.id, "заметок пока нет")
@bot.message_handler(commands=["del"])
def del_note(message):
    number = message.text.replace("/del", "").strip()
    
    if not number.isdigit():
        bot.send_message(message.chat.id, "напиши номер: /del 2")
        return
    if os.path.exists("notes.json"):
        with open("notes.json" , "r", encoding="utf-8") as file:
            notes = json.load(file)
        index = int(number) - 1
        if 0 <= index < len(notes):
            notes.pop(index)
            with open("notes.json", "w" ,   encoding="utf-8")as file:
                json.dump(notes, file, ensure_ascii=False)
            bot.send_message(message.chat.id, "удалил заметку: " + number)
        else:
            bot.send_message(message.chat.id," такой заметки нет")
    else:
        bot.send_message(message.chat.id, "пока заметок нет")
@bot.message_handler(commands=["count"])
def count_notes(message):
    if os.path.exists("notes.json"):
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
        bot.send_message(message.chat.id, f"У тебя {len(notes)} заметок")
    else:
        bot.send_message(message.chat.id, "заметок пока нет")

@bot.message_handler(commands=["clear"])
def clear_notes(message):
    if os.path.exists("notes.json"):
        os.remove("notes.json")
        bot.send_message(message.chat.id, "все заметки удалены")
    else:
     bot.send_message(message.chat.id, "и так пусто")
@bot.message_handler(commands=["help"])
def help_command(message):
     text = (
         "Мои команды:\n"
         "/start - начать:\n"
         "/save текст - сохранить заметку:\n"
         "/list - показать заметки:\n"
         "/clear - удалить все заметки:\n"
         "del - удалить определенную заметку:\n"
         "а еще я понимаю:\n"
         "привет, пока, погода, шутка, время"
      )
     bot.send_message(message.chat.id, text)    
@bot.message_handler(func=lambda message:True)
def answer(message):
    text = message.text.lower( )
    if text == "привет":
        bot.send_message(message.chat.id, "здравия желаю, товарищ!")
    elif text == "пока":
        bot.send_message(message.chat.id, "до связи")
    elif text == "погода":
        response = requests.get("https://wttr.in/Moscow?format=3")
        bot.send_message(message.chat.id, response.text)
    elif text == "время":
        now = datetime.datetime.now()
        bot.send_message(message.chat.id ,now.strftime("%H:%M:%S"))
    elif text == "шутка":
        response = requests.get("https://api.chucknorris.io/jokes/random")
        data = response.json()
        bot.send_message(message.chat.id, data["value"])
    else:
       bot.send_message(message.chat.id, "не понял")
bot.polling()

