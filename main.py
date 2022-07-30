import os
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup

my_secret = os.environ['API_KEY']
bot = telebot.TeleBot(my_secret)

#get user input
def user_input(message):
  request = message.text.split()
  if len(request) < 1:
    return False
  else:
    return True

@bot.message_handler(func=user_input)
def search_movie(message):
  request = message.text
  keyboard = types.InlineKeyboardMarkup()
  #print(request.replace(" ", "+"))
  
  #search for movie to only get id
  url = "https://www.repelisplus.id/buscar/" + str(request)
  print(url)
  data = requests.get(url)

  movie_title = []
  movie_url = []

  #get movie id with selector
  html = BeautifulSoup(data.text, 'html.parser')
  movies = html.select('div.ksaj')

  #get all elements with loop form websiote
  for movie in movies:
    title = movie.select('.kaiz')[0].get_text()
    url = movie.select('.ksaj > a')[0]
    
    #add info movie to array 
    movie_title.append(title)
    movie_url.append(url['href']+"online")

  for x in range(0, len(movie_title)):

    url_button = types.InlineKeyboardButton(text= movie_title[x], url=movie_url[x])
    keyboard.add(url_button)

    
  if len(movie_title) == 0:
    bot.reply_to(message, "No matches found for: " + request)
  else:
    bot.reply_to(message, "Matches found for: " + request, reply_markup=keyboard)

bot.polling()
