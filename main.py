import requests
import datetime
import time
import os
import telebot
from telebot import apihelper

from requests.packages.urllib3.exceptions import InsecureRequestWarning

from config import *

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Comment string below if you do not use proxy
apihelper.proxy = apihelper_proxy

headers = grafana_token
path = image_path


def download_image(dasboard, panelId, user_id):
#   time offsets
    six_hours = datetime.timedelta(hours=6)
    twelve_hours = datetime.timedelta(hours=12)

#   human date
    now = datetime.datetime.now()
    now6 = datetime.datetime.now() - six_hours
    now12 = datetime.datetime.now() - twelve_hours

    stimpenow = str(time.mktime(now.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe6 = str(time.mktime(now6.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    stimpe12 = str(time.mktime(now12.timetuple())).split('.')[0] + str(float(now.microsecond) / 1000000).split('.')[1][0:3]
    url6 = grafana_url + '/render/dashboard-solo/db/' + dasboard + '?orgId=1&from=' + stimpe6 + '&to=' + stimpenow + '&panelId=' + panelId + '&width=1000&height=500'
    url12 = grafana_url + '/render/dashboard-solo/db/' + dasboard + '?orgId=1&from=' + stimpe12 + '&to=' + stimpenow + '&panelId=' + panelId + '&width=1000&height=500'
    for url in url6, url12:
        now = datetime.datetime.now()
        filedate = now.strftime("%Y%m%d_%I-%M-%S-%m")
        r = requests.get(url, verify = False, headers = headers, timeout = 30)
        folder = path + str(user_id) + "/"
        if os.path.exists(folder) is False:
            os.mkdir(folder)
        out = open(folder + str(dasboard) + "_" + filedate + ".png", "wb")
        out.write(r.content)
        out.close()
        time.sleep(0.12)


token = bot_token
bot = telebot.TeleBot(token)


user_markup0 = telebot.types.ReplyKeyboardMarkup()
user_markup0.row('/start')

user_markup = telebot.types.ReplyKeyboardMarkup()
user_markup.row('bot-testing-dashboard', 'open-dashboard')


white_list = user_list


def check_user(user):
    use = check
    if use == 1:
        if user in white_list:
            return True
        else:
            return False
    else:
        return True


commands = command_list


def remove_img(user_id):
    directory = path + str(user_id) + "/"
    files = os.listdir(directory)
    for i in files:
        os.remove(directory + i)


@bot.message_handler(commands=['start'])
def handle_start(message):
    if check_user(message.from_user.id) is True:
        bot.send_message(message.from_user.id, 'Starting', reply_markup=user_markup)
    else:
        bot.send_message(message.from_user.id, 'What is your name?', reply_markup=user_markup0)


@bot.message_handler(content_types=['text'])
def handle_text(message):

    def send_photo(user_id):
        directory = path + str(user_id) + "/"
        files = os.listdir(directory)
        for i in files:
            now = datetime.datetime.now()
            img = open(directory + i, 'rb')
            arr = str(now) + ',' + str(message.from_user.id) + ',' + str(message.text) + ', ' +  str(img)
            log = open(logfile, 'a')
            log.write(arr + '\n')
            log.close()
            bot.send_photo(message.from_user.id, img)
            img.close()

    def logging():
        now = datetime.datetime.now()
        log = open(logfile, 'a')
        arr = str(now) + ',' + str(message.from_user.id) + ',' +  u''.join((message.text)).encode('utf-8').strip()
        log.write(arr + '\n')
        log.close()

    def handle_message(dashboard, lst):
        for panelId in lst:
            download_image(dashboard, panelId, user_id = message.from_user.id)
        send_photo(message.from_user.id)
        remove_img(message.from_user.id)

#   Unauthorized users banner
    if check_user(message.from_user.id) is False:
        if message.text != 'Pwd12':
            bot.send_message(message.from_user.id, 'You are not user of bot. Enter password or contact with administrators', reply_markup=user_markup0)
            logging()
#           who is try to use bot
            bot.forward_message(admin_id, message.chat.id, message.message_id)
            bot.send_message(admin_id, "User " + str(message.from_user.id) + " want to use this bot")
        else:
#       Adding user at white list by password
            white_list.append(message.from_user.id)
            bot.send_message(message.from_user.id, 'Password accepted. You are at user list now')


    else:

#   Adding user at white list by current user
        if message.text.isdigit() is True and len(message.text)>=8:
            try:
                bot.send_message(message.text, 'you are add at user list') # sayind new user about his adding in white list
                white_list.append(int(message.text))
                bot.send_message(message.from_user.id, str(white_list))
            except:
                bot.send_message(message.from_user.id, 'Coudnt add user')

#   Get list of all users
        if message.text == 'List':
            bot.send_message(message.from_user.id, str(white_list))

#   Uncorrect command handling
        if message.text not in commands:
            bot.send_message(message.from_user.id, 'Please type start command', reply_markup=user_markup)

#   Bot stop pooling
        if message.text == 'Stop' and check_user(message.from_user.id) is True:
            os.kill(os.getpid(), 9)

#   Dashboar handling. Main functional
        if message.text == 'bot-testing-dashboard':
            user_markup2 = telebot.types.ReplyKeyboardMarkup()
            user_markup2.row('Carbon agents localdomain', 'Metric recieved')
            user_markup2.row('go back')
            bot.send_message(message.from_user.id, 'going to Carbon agents localdomain dashboard', reply_markup=user_markup2)

        if message.text in ['Metric recieved', 'Carbon agents localdomain'] and message.from_user.id in white_list:
            dashboard = 'bot-testing-dashboard'
            if message.text == 'Carbon agents localdomain':
                panelId = ('1')
            if message.text == 'Metric recieved':
                panelId = ('2')
            handle_message(dashboard, panelId)

        if message.text == 'open-dashboard':
            user_markup3 = telebot.types.ReplyKeyboardMarkup()
            user_markup3.row('Commited points', 'Memussage')
            user_markup3.row('go back')
            bot.send_message(message.from_user.id, 'going to open-dashboard', reply_markup=user_markup3)

        if message.text in ['Commited points', 'Memussage'] and message.from_user.id in white_list:
            dashboard = 'open-dashboard'
            if message.text == 'Commited points':
                panelId = ('1')
            if message.text == 'Memussage':
                panelId = ('2')
            handle_message(dashboard, panelId)

        if message.text == 'go back':
            bot.send_message(message.from_user.id, 'going back', reply_markup=user_markup)

if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=30)


