import telebot
#---------------#
TOKEN = ""
bot = telebot.TeleBot(TOKEN)
#---------------#

#---------------#
bot.polling(True)