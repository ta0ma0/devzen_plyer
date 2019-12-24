
import curses
import os
import re
import time
from curses import panel
from bs4 import BeautifulSoup
from parse_html import  get_menu_list, get_timings, time_to_seconds, \
main_menu_items_funct, list_of_themes_end, text_discription_get, time_to_seconds, \
vlc_start
from get_files import get_page_of_day, list_day_podcasts, file_name, parse_main_page, get_mp3_from_page

"""В скрипт импортируется тестовый модуль, который работает с локальным файлом подкаста test_print.py"""


class Menu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(5,2)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(['Выход'])

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        global page, list_of_themes, timing_list_var, list_of_themes_end_temp, sub_menu_items
        global sub_menu_items
        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):

                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                msg = '%d. %s' % (index, item)
                self.window.addstr(10+ index, 1, msg, mode)
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    epis = page[self.position]
                    global page_var
                    global timing_list_var
                    global podcast_link
                    page_var = open(epis, 'r')
                    # file = get_mp3_from_page(page_var)
                    list_of_themes = get_menu_list(page_var)
                    timing_list_var = get_timings(list_of_themes) #Получаем список таймингов в формате [hh:mm:ss]
                    list_of_themes_end_temp = list_of_themes_end(list_of_themes)
                    global sub_menu_items
                    sub_menu_items = main_menu_items_funct(list_of_themes_end_temp, "command")
                    page_var.close()
                    # self.window.addstr(30, 1, sub_menu_items[0][0])
                    page_var = open(epis, 'r')
                    podcast_link = get_mp3_from_page(page_var)
                    page_var.close()
                    stdscreen = curses.newwin(150, 400)
                    self.window.addstr(40, 1, podcast_link)
                    submenu = SubMenu(sub_menu_items, stdscreen) #Вывел конкретный подкаст, нужно изменить на выбор подкастов.

                    submenu.display_sub()
                    self.items[self.position]
                    self.window.clear()
            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)
        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class SubMenu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(5,2)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(['[Назад]'])

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display_sub(self):

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):

                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                next = 1
                for disript in text_discription_get():
                    self.window.addstr(next, 1, disript)
                    next +=1
                msg = '%d. %s' % (index, item[0])
                if index < 10:
                    msg = '%d. %s' % (index, " " + item[0])
                self.window.addstr(10+ index, 1, msg, mode)
            key = self.window.getch()
            if key in [curses.KEY_ENTER, ord('\n')]:

                # # vlc_start(time_sec, file)
                if self.position == len(self.items)-1:
                    break
                else:

                    time_sec = time_to_seconds(timing_list_var, self.position)
                    # time.sleep(5)
                    vlc_start(time_sec, podcast_link)

                    self.window.clear()
                    # self.items[self.position][1]()
            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)
            self.window.clear()
            self.panel.hide()
            panel.update_panels()
            curses.doupdate()

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)
        dict_podcasts = parse_main_page()
        url = 'https://devzen.ru/'
        get_page_of_day(url)
        # choise_epis ='episode-0263.html'
        # file = "devzen-0263-2019-10-19-def77df75c4ecc54.mp3"
        # page = GetPageChoise(choise_epis)
        # list_of_themes = get_menu_list(page)
        # timing_list_var = (get_timings(list_of_themes)) #Получаем список таймингов в формате [hh:mm:ss]
        # list_of_themes_end_temp = list_of_themes_end(list_of_themes)
        # sub_menu_items = main_menu_items_funct(list_of_themes_end_temp) #Заглушка echo, будет запускать VLC
        global page
        page = file_name(dict_podcasts)
        list_main_menu_item = []
        # submenu_items = [# Объявлено в начале программы
        #         ('beep', curses.beep),
        #         ('flash', curses.flash)
        #]
        main_menu_list = list_day_podcasts()
        # sub_menu_items =


        # main_menu_items = [
        #         ('beep', curses.beep),
        #         ('flash', curses.flash),
        #         ('submenu', submenu.display_sub)
        #         ]
        # sub_menu_items = []

        list_tuple = []
        for item in main_menu_list:
            # el_tuple = tuple([item, submenu.display_sub])
            el_tuple = item
            list_main_menu_item.append(el_tuple)

        main_menu = Menu(list_main_menu_item, self.screen)
        # print(file_name(dict_podcasts))
        # print(page[0])
        # print(get_menu_list(page))
        # page = open('episode-0272.html', 'r')
        # print(get_menu_list(page))
        # page_var = open("episode-0272.html", 'r')
        # list_of_themes = get_menu_list(page_var)
        # print(list_of_themes)
        # print(get_mp3_from_page(page))
        # time.sleep(5)
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(MyApp)
#Вывел меню, сделал выбор, нужно вывести Discription, сделать вызов плеера по выбору темы.
