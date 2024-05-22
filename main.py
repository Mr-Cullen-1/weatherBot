import telebot
import requests
import json


bot = telebot.TeleBot('token')
API_KEY = 'Weather API KEY'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome! Write name of origin:')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data['main']['temp']
        bot.reply_to(message, f'Weather: {temp}')

        image = 'sun.png' if temp > 10.0 else 'sunny.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, photo=file)
    else:
        bot.send_message(message.chat.id, f'Error: City not found! Try again')


bot.polling(none_stop=True)
