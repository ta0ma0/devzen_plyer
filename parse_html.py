import curses
import re
import os
import textwrap
from bs4 import BeautifulSoup
text_discription = []
timing_list = []
seconds_vlc = []



def get_menu_list(page_var):
    """Берем тайминги с выбранного подкаcта, за одно описание"""
    global timing_list
    global timing_display
    timing_display = []
    list_of_themes = []
    """Получаем данные о подкасте"""
    soup = BeautifulSoup(page_var, 'html.parser')
    get_timing = soup.find_all('div', {'class': 'entry-content'})
    for div in get_timing:
        discription = div.find_all('p')
        text_discription.append(discription[1].text)
        """Получаем тайминги из <ul>"""
        theme = div.find_all('li')
        theme = theme[1:]
        count = 1
        for el in theme:
            theme_list = str(el)
            if re.search('<li>\[', theme_list) and count == 1:
                list_of_themes.append(el.text)
        return list_of_themes


def list_of_themes_end(list_of_themes_var):
    list_of_themes_end = []
    for el in list_of_themes_var:
        mylist = el.split("\n")
        # print(mylist)
        for el2 in mylist:
            if re.match('\[', el2):
                list_of_themes_end.append(el2)
    return list_of_themes_end


def get_timings(list_of_themes_var):
    for el in list_of_themes_var:
        pre_timing_list = re.findall('\d{2}:\d{2}:\d{2}', el)
        timing_list.append(pre_timing_list)
    return timing_list


def time_to_seconds(timing_list, index): #Получаем время в секундах начала воспроизведения по индексу пункта меню.
    for el in timing_list:
        pre_sec = el[0].split(":")
        hour = int(pre_sec[0]) * 3600
        min = int(pre_sec[1]) * 60
        sec = int(pre_sec[2])
        seconds = hour + min + sec
        seconds_vlc.append(str(seconds))
    seconds_start_vlc = seconds_vlc[index]
    return seconds_start_vlc


def vlc_start(time_sec, file):
    """Запускаем плеер с указанного времени"""
    os.system('vlc --start-time={} {} > /dev/null 2>&1'.format(time_sec, file))

def main_menu_items_funct(list_of_themes, command):
    """Функция для построения списка кортежей, где первый элемент пункт меню, а второй команда запуска плеера"""
    main_menu_items = []
    for el in list_of_themes:
        item_menu = (el, command)
        main_menu_items.append(item_menu)
    return main_menu_items

def text_discription_get(): #Разбиваем строку га список по 120 символов
    text_discription_end = textwrap.wrap(text_discription[0], width=120)
    return text_discription_end

def text_discription_string(): #Превращаем описание в строку с переносами
    discription_list = []
    for item in text_discription_get():
        discription_srt_raw = item + '\n'
        discription_list.append(discription_srt_raw)
    discription_srt = str(discription_list).strip('[]')
    return discription_srt
