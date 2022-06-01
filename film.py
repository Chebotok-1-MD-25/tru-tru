import requests
import bs4
from telebot import types



# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать фильм":
        send_film(bot, chat_id)

    elif ms_text == "Билеты на сегодня":
        today_film(bot, chat_id)



# -----------------------------------------------------------------------
def send_film(bot, chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)
# --------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

def today_film(bot, chat_id):
    main_link = "https://spb.kinoafisha.info"
    url = "https://spb.kinoafisha.info/movies/"
    responsive = requests.get(url)
    soup = bs4.BeautifulSoup(responsive.text, "html.parser")
    all_films = soup.find_all('div', class_="movieList movieList-grid grid")
    for block in all_films:
        block_film = block.find_all('div', class_="movieList_item movieItem  movieItem-grid grid_cell4")
        for info in block_film:
            info_film = info.find_all('div', class_="movieItem_info")
            for name in info_film:
                name_film = name.find_all('a').get_text(strip=True)
            for action in info_film:
                action_film = action.find_all('div', class_="movieItem_actions")
                for button in action_film:
                    button_film = button.find_all('button')
                    for link in button_film:
                        link_film = main_link + link.find_all('a').get('href')
                        film = f"{name_film} \n Купить билет: {link_film}"
                        bot.send_message(chat_id, film)


    #markup = types.InlineKeyboardMarkup()
    #btn1 = types.InlineKeyboardButton(text="<Билеты>", url=link_film)
    #markup.add(btn1)
    #bot.send_message(chat_id, text=name_film, parse_mode='HTML', reply_markup=markup)

