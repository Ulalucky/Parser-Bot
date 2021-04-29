import requests
import telebot
from bs4 import BeautifulSoup
from decouple import config
from urllib3.util import url

from keyboards.inline import inline_keyboard

bot = telebot.TeleBot(config('TOKEN'))

BASE_URL = 'https://www.eldorado.ru/c/smartfony/'

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_keyboard = InlineKeyboardMarkup(row_width=4)
for i in range(4):
    btn1 = InlineKeyboardButton(str(i*4 +1), callback_data=(i*4+1))
    btn2 = InlineKeyboardButton(str(i*4 +2), callback_data=(i*4+2))
    btn3 = InlineKeyboardButton(str(i*4 +3), callback_data=(i*4+3))
    btn4 = InlineKeyboardButton(str(i*4 +4), callback_data=(i*4+4))
    inline_keyboard.add(btn1, btn2, btn3, btn4)

title = {}
images = {}
price = {}

def get_url(url):
    headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url, headers=headers)
    return response.text

def get_soup(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup

titlek = InlineKeyboardMarkup()
@bot.message_handler(commands=['start' ,])
def welcome(message):
    global title, images, price
    chat_id = message.chat.id
    html = get_url(BASE_URL)
    soup = get_soup(html)
    info = soup.find("div", class_="ListingContent_listingContentWrapper__37KSE").find("ul", class_="GridInner_list___8u79").find_all("li", class_='ListingProductCardList_productCardListingWrapper__3-o9i')
    count = 0

    while count < 16:
        for i, a in enumerate(info, len(title) + 1):
            title[i] = a.find("a", class_="ListingProductCardList_productCardListingLink__1JIMi").text
            images[i] = a.find("a", class_="ListingProductCardList_productCardListingImageContainer__FqE33").find("img").get("src")
            price[i] = a.find("div", class_="PriceBlock_buyBoxPriceBlock__dpI5A PriceBlock_buyBoxPriceBlockStyledAvailable__1XDmA").find("span", class_="PriceBlock_buyBoxPrice__3QGyj PriceBlock_buyBoxPriceStyled__29J_G").text
            btn = InlineKeyboardButton(title[i], callback_data=i)
            titlek.add(btn)
            count += 1
            if count >= 16:
                break

    bot.send_message(chat_id, 'phones', reply_markup=titlek)


@bot.callback_query_handler(func=lambda c:True)
def cal_inline(c):
    chat_id = c.message.chat.id
    for i in range(1, 17):
        ititle = title[i]
        iphoto = images[i]
        iprice = price[i]
        if c.data == str(i):
            bot.send_message(chat_id, ititle)
            bot.send_message(chat_id, iphoto)
            bot.send_message(chat_id, iprice)

bot.polling(none_stop=True)
