import telebot
from bs4 import BeautifulSoup
import requests
import time
from threading import Thread
from message import Comment
import telegram


bot = telebot.TeleBot("MY TOKEN")


@bot.message_handler(commands=['start', 'help'])
def get_text_messages(message):
    main_function(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "Я не понимаю команды \"" + m.text + "\"\nМожете воспользоваться командой /help")


def check_ad(s: str):
    list = ['Что вы думаете', 'подписывайтесь', 'Подписывайтесь', 'на канал', 'terricon.com', 'Youtube', 'делитесь',
            'смотреть онлайн', 'поставить лайк', 'подписаться', 'ставьте лайк']
    for tmp in list:
        if tmp in s:
            return True
    return False


def for_send(comment: Comment):
    if comment.minute != '':
        s = comment.minute + "'\n " + comment.text + '\n' + comment.time
        # s = comment.minute + "' (" + comment.time + ")\n " + comment.text
    else:
        s = comment.text + '\n' + comment.time
        # s = comment.time + "\n " + comment.text
    return s


def parse(message):
    # url = r'https://terrikon.com/football/matches/62526/online'
    # url = r"https://terrikon.com/football/matches/62524/online"
    url = r"https://terrikon.com/football/matches/63132/online"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    online_table = soup.find('table', {'class': 'online_table'})
    translation = []
    table_comments = online_table.findAll('tr')
    for tmp in table_comments:
        line = tmp.findAll('td')
        if len(line) != 3:
            continue
        cellOne = line[0].text.split()
        minute = ""
        if len(cellOne) == 2:
            minute = cellOne[0]
            time = cellOne[1]
        else:
            time = cellOne[0]
        is_img = line[1].find('img')
        img = ""
        if is_img:
            img = is_img.get('src')
        text = line[2].text
        if (not check_ad(text)) and (text.strip() != '') and \
                (line[2].find('blockquote', {'class': 'twitter-tweet'}) is None):
            comm = Comment(minute, time, img, text)
            translation.append(comm)
    '''for tmp in translation:
        bot.send_message(message.from_user.id, for_send(tmp))'''
    return translation


def send(message, comments):
    bot.send_message(message.from_user.id, for_send(comments))


def streaming(message):
    print("in streaming")
    current_list = []
    while True:
        comments = parse(message)
        comments.reverse()
        print("!!", current_list != comments)
        if current_list != comments:
            for tmp in comments[len(current_list):]:
                send(message, tmp)
            current_list = comments
        time.sleep(5)


def main_function(message):
    thread1 = Thread(target=streaming, args=(message,))
    thread1.start()


bot.polling(none_stop=True, interval=0)
