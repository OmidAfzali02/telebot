import telebot as tel
from telebot import types
import os
import random
from PIL import ImageGrab
from winsound import Beep
from playsound import playsound
from datetime import datetime


# cpu_usage = os.popen("wmic cpu get loadpercentage").read() # for getting the percentage of cpu use

class Data:
    user_want_to_restart = 0
    user_want_to_shutdown = 0


os.system("cls")
TOKEN = ""
bot = tel.TeleBot(TOKEN)


# for reading admin files
def getfile(filename):
    myfile = open(filename, "r+")
    return myfile.read()
    myfile.close()


# for saving data in a database
def putfile(filename, filedata):
    myfile = open(filename, "w+")
    return myfile.write(filedata)
    myfile.close()


print("bot is ready")


def start(user, check):
    sender_chatid = user.chat.id

    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("Take a screen shot")
    markup2 = types.KeyboardButton("Power Options")
    markup3 = types.KeyboardButton("Play sound")
    markup4 = types.KeyboardButton("File manager")
    markups.add(markup1, markup2, markup3, markup4)

    if check == 1:
        bot.send_message(sender_chatid, "🏘Home", reply_markup=markups)
    else:
        bot.send_message(sender_chatid, "Welcome to AlphaPAI OS Remote", reply_markup=markups)


def poweroptions(user):
    sender_chatid = user.chat.id

    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("Shutdown")
    markup2 = types.KeyboardButton("Restart")
    markup3 = types.KeyboardButton("🏘Home")
    markups.add(markup1, markup2, markup3)
    bot.send_message(sender_chatid, "Welcome to power options", reply_markup=markups)


def takescreenshot(user):
    sender_chatid = user.chat.id

    bot.send_message(sender_chatid, "🙂Taking a screen shot...")
    ThisIsPhoto = ImageGrab.grab()
    ThisIsPhoto.save("screenshot.png")
    bot.send_message(sender_chatid, "😊Screenshot was taken :)\n◼️ Sending to you soon...")
    photo = open("screenshot.png", "rb")

    bot.send_photo(sender_chatid, photo, caption="your screen shot")
    photo.close()
    os.remove("screenshot.png")
    start(user, 1)


def play_sound(user):
    sender_chatid = user.chat.id

    # for playing specified mp3 file
    # bot.send_message(sender_chatid, "Playing... ")
    # playsound("music.mp3")

    bot.send_message(sender_chatid, "Playing...")
    for x in range(1, 5):
        Beep(1000 * x, 200)
        Beep(1000 * x, 200 - (x * 50))
    bot.send_message(sender_chatid, "Done!")


def save_note(user):
    sender_chatid = user.chat.id
    sender_text = user.text

    thetext = sender_text.replace("/save ", "")

    randomnumber = random.randint(11111, 99999)
    putfile("database/data_" + str(randomnumber) + ".txt", str(thetext))
    bot.send_message(sender_chatid, f"Payame Shoma Ba ID {str(randomnumber)}  Zakhire Shod.")


def shutdown_btn(user):
    Data.user_want_to_restart = 0
    Data.user_want_to_shutdown = 1
    sender_chatid = user.chat.id

    bot.send_message(
        sender_chatid, "Are you sure to shutdown your computer ?\nSend /yes to shutdown or send /no to")


def restart_btn(user):
    Data.user_want_to_restart = 1
    Data.user_want_to_shutdown = 0

    sender_chatid = user.chat.id

    bot.send_message(
        sender_chatid, "Are you sure to restart your computer ?\nSend /yes to restart or send /no to")


def shutdown_or_restart(user):
    sender_chatid = user.chat.id

    if (Data.user_want_to_shutdown == 1 and Data.user_want_to_restart == 0):
        bot.send_message(sender_chatid, "Your Computer Is Shutting Down...")
        Data.user_want_to_shutdown = 0
        Data.user_want_to_restart = 0
        # os.system("shutdown /s /t 1")
    elif (Data.user_want_to_restart == 1 and Data.user_want_to_shutdown == 0):
        Data.user_want_to_shutdown = 0
        Data.user_want_to_restart = 0
        bot.send_message(sender_chatid, "Your Computer Is Restarting...")
        # os.system("shutdown /r /t 1") #Restart The System
    else:
        bot.send_message(sender_chatid, "!!! ERROR To Process !!!")


def no_to_shutdown(user):
    sender_chatid = user.chat.id

    Data.user_want_to_restart = 0
    Data.user_want_to_shutdown = 0
    bot.send_message(sender_chatid, "Done !")


def saved_notes(user):
    sender_chatid = user.chat.id

    listfiles = ""
    for r, d, f in os.walk("database"):
        for file in f:
            listfiles = listfiles + "\n" + str(file)
    bot.send_message(sender_chatid, "Your save list :\n" + str(listfiles))


def filemanager(user):
    sender_chatid = user.chat.id
    markups = types.ReplyKeyboardMarkup(row_width=2)
    markup1 = types.KeyboardButton("🏘 Home")
    markup2 = types.KeyboardButton("📥 Download")
    markup3 = types.KeyboardButton("🗂 File List")
    markups.add(markup2, markup3, markup1)
    bot.send_message(sender_chatid, "Welcome to filemanager", reply_markup=markups)


def downloadfile(user):
    sender_chatid = user.chat.id
    bot.send_message(sender_chatid, "Usage :\n/download [file name/file adress]")


def download_this_file(user):
    sender_chatid = user.chat.id
    sender_text = user.text
    filename_or_fileadress = sender_text.replace("/download ", "")
    if os.path.isdir(str(filename_or_fileadress)):
        bot.send_message(sender_chatid, "This is folder :)")
    else:
        if os.path.isfile(str(filename_or_fileadress)):
            bot.send_message(sender_chatid, "Downloading " + str(filename_or_fileadress) + "...")
            thefile = open(filename_or_fileadress, "rb")
            bot.send_document(sender_chatid, thefile, caption="This is your file")
        else:
            bot.send_message(sender_chatid, "Not Found")
            pass


def justfilelist(user):
    sender_chatid = user.chat.id
    bot.send_message(sender_chatid, "Usage:\n/filemanager [dir]")


def filemanagerlist(user):
    sender_chatid = user.chat.id
    sender_text = user.text

    directory = sender_text.replace("/filemanager ", "")

    if os.path.isdir(directory):
        bot.send_message(sender_chatid, "🔎 Scanning....")

        foldercount = 0
        folderlist = ""

        filecount = 0
        filelist = ""

        for r, d, f in os.walk(directory):
            for folder in d:
                if foldercount > 30 or foldercount == 30:
                    break
                else:
                    if "\\" in r:
                        pass
                    else:
                        foldercount += 1
                        folderlist = folderlist + "\n" + "📁 " + r + "/" + folder
            for file in f:
                if filecount > 30 or filecount == 30:
                    break
                else:
                    filecount += 1
                    filelist = filelist + "\n" + "🧾 " + r + "/" + file
        bot.send_message(sender_chatid, "🗂 30 First Folders In " + directory + " : \n\n" + str(folderlist))
        bot.send_message(sender_chatid, "🗃 30 First File In " + directory + " : \n\n" + str(filelist))
    else:
        bot.send_message(sender_chatid, "I can't find this directory  :(")


@bot.message_handler(content_types=['text'])
def botmain(user):
    # creator = getfile("admin.txt").splitlines()[0]
    # print(creator)
    sender_chatid = user.chat.id
    sender_text = user.text

    # adding security parameters for admins
    # if str(sender_chatid) in creator and os.getlogin() == "Ranger Omid":
    #     bot.send_message(sender_chatid, "Hello my creator")
    # else:
    #     bot.send_message(sender_chatid, "hey there")

    if sender_text == "/start" or sender_text == "🏘Home":
        if sender_text == "🏘Home":
            check = 1
            start(user, check)
        else:
            check = 2
            start(user, check)
    if sender_text == "/khobi":
        bot.send_message(sender_chatid, "مرسی تو خوبی")
    if sender_text == "/save":
        bot.send_message(sender_chatid, "Tarze Estefade :\n/save [message]")
    if sender_text.startswith("/save "):
        save_note(user)
    if sender_text == "/savelist":
        saved_notes(user)
    if sender_text == "Power Options":
        poweroptions(user)
    if sender_text == "Take a screen shot":
        takescreenshot(user)
    if sender_text == "Play sound":
        play_sound(user)
    if sender_text == "Shutdown":
        shutdown_btn(user)
    if sender_text == "Restart":
        restart_btn(user)
    if sender_text == "/yes":
        shutdown_or_restart(user)
    if sender_text == "/no":
        no_to_shutdown(user)
    if sender_text == "File manager":
        filemanager(user)
    if sender_text.startswith("/download "):
        download_this_file(user)
    if sender_text == "/download" or sender_text == "📥 Download":
        downloadfile(user)
    if sender_text == "🗂 File List" or sender_text == "/filemanager":
        justfilelist(user)
    if sender_text.startswith("/filemanager "):
        filemanagerlist(user)


bot.polling(none_stop=True, interval=0)
