import os
import re

import requests
from bs4 import BeautifulSoup

url = 'https://devzen.ru/'
url_podcast = ''
file_name_podcast = ''
file_name_list = []
r = requests.get(url)
text_discription = []
headers_menu = []


def get_page_of_day(url_head):
    r = requests.get(url_head)
    with open("index.html", 'wb') as output_file:
        output_file.write(r.text.encode('utf8'))


def get_all_podcasts(url_podcast, file_name_podcast):
    r = requests.get(url_podcast)
    with open(file_name_podcast, 'wb') as output_file:
        output_file.write(r.text.encode('utf8'))
    return print("Файл ", file_name_podcast, " сохранен")


def list_day_podcasts():
    page = open('index.html', 'r')
    page_var = page.read()
    soup = BeautifulSoup(page_var, 'html.parser')
    get_content = soup.find('div', {'id': 'content'})
    for div in get_content.find_all('h1'):
        headers = div.find_all('a')[0].text
        match = re.findall('Episode | episode', headers)
        try:
            # headers_menu = []
            if match[0] == 'Episode' or 'episode':
                headers_menu.append(headers)
        except IndexError:
            pass
    return headers_menu


def menu_podcast_of_day():
    number_list = 1
    global pod_dict
    pod_dict = {}
    for el in file_name_podcast:
        pod_dict[number_list] = el
        number_list += 1


def file_name(name_dict):
    name_url = name_dict.values()
    for item in name_url:
        item = str(item)
        file_name_list.append(item.split('/')[3] + '.html')
    return file_name_list


def lst_dir():
    on_hdd = os.listdir(".")
    return on_hdd


def get_mp3_from_page(page_var):
    soup = BeautifulSoup(page_var, 'html.parser')
    get_audio = soup.findAll('div', class_="powerpress_player")
    if get_audio is None:
        get_audio = soup.find_all('audio')
    podcast_link = ""
    for item in get_audio:
        podcast_link = item.find('a').get('href')
    return podcast_link


def parse_main_page():
    page = open('index.html', 'r')
    page_var = page.read()
    soup = BeautifulSoup(page_var, 'lxml')
    title_list = soup.find_all('h1', {'class': 'entry-title'})
    global podcast_link_list
    global dict_podcasts
    name_dict = {}
    podcast_name_list = []
    podcast_link_list = []
    dict_podcasts = {}
    for item in title_list:
        podcast_name = item.find('a').text
        podcast_link = item.find('a').get('href')
        match = re.findall('Episode | episode', podcast_name)
        try:
            if match[0] == 'Episode' or 'episode':
                podcast_name_list.append(podcast_name)
                podcast_link_list.append(podcast_link)
        except IndexError:
            pass
    dict_podcasts = dict(zip(podcast_name_list, podcast_link_list))
    url_podcast = podcast_link_list
    return dict_podcasts


get_page_of_day(url)
on_hdd = lst_dir()

parse_main_page()

file_name_podcast = file_name(dict_podcasts)
url_podcast = podcast_link_list

for el in file_name_podcast:
    print("")
    if el in on_hdd:
        print("")
    else:
        try:
            url_podcast_end = url + el[0:12]
            print(url_podcast_end)
        except IndexError as err:
            print("Возможно статей стало больше 9999: ", err)
        file_name_podcast_end = el
        get_all_podcasts(url_podcast_end, file_name_podcast_end)
