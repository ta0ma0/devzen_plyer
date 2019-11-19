import requests
from bs4 import BeautifulSoup
import re
import os
import shutil
import textwrap
url = 'https://devzen.ru/'
url_podcast = ''
file_name_podcast = ''
file_name_list = []
r = requests.get(url)
text_discription = []

def get_page_of_day(url_head):
    r = requests.get(url_head)
    with open("index.html", 'wb') as output_file:
        output_file.write(r.text.encode('utf8'))


def get_all_podcasts(url_podcast, file_name_podcast ):
    """Сохраняем странички подкастов для локального парсинга"""
    r = requests.get(url_podcast)
    with open(file_name_podcast, 'wb') as output_file:
        output_file.write(r.text.encode('utf8'))
    return print("Файл ", file_name_podcast, " сохранен" )





def list_day_podcasts():
    """Список подкастов на главной"""
    get_content = soup.find('div', {'id': 'content'})
    for div in get_content.find_all('h1'):
        headers = div.find_all('a')[0].text
        # description = div.find('a').text
        # text_discription.append(discription[1].text)   #Описание подкаста идет вторым тегом <p
        print(headers)


def file_name (name_dict):
    name_url = name_dict.values()
    for item in name_url:
        item = str(item)
        file_name_list.append(item.split('/')[3] + '.html')
    return file_name_list


def lst_dir():
    """Получим файлы страниц подкастов на диске, чтобы не качать повторно"""
    on_hdd = os.listdir(".") #В коченчном варианте поправить путь до текущей директории.
    return on_hdd


def get_mp3_from_page ():
    """Получаем данные о подкасте"""
    soup = BeautifulSoup(page_var2, 'html.parser')
    get_audio = soup.find_all('audio')
    for item in get_audio:
        podcast_link = item.find('a').get('href')
    return podcast_link


def file_name_mp3 (podcast_link):
    """Формируем имя локального файла"""
    name_url = podcast_link
    try:
        podcast_link1 = name_url.split('/')[5]
    except IndexError:
        podcast_link1 = name_url.split('/')[4]
    return podcast_link1


def get_mp3_podcasts(url_podcast, file_name_mp3):
    """Скачиваем файл подкаса"""
    print("Качаем подкаст, подождите...")
    try:
        r = requests.get(url_podcast, stream=True)
    except Exception as err:
        print("Загрузка не удалась: ", err)
    with open(file_name_mp3, 'wb') as output_file:
        shutil.copyfileobj(r.raw, output_file)
    del r
    return print("Файл ", file_name_mp3, " сохранен")


def get_timing(page_var):
    global timing_list
    timing_list = []
    global timing_display
    timing_display = []
    """Получаем данные о подкасте"""
    soup = BeautifulSoup(page_var, 'html.parser')
    get_timing = soup.find_all('div', {'class': 'entry-content'})
    for div in get_timing:
        discription = div.find_all('p')
        text_discription.append(discription[1].text)   #Описание подкаста идет вторым тегом <p>, получаем его по индексу.
        """Получаем тайминги из <ul>"""
        timing = div.find('ul').text
        timing_display.append(timing)
        """Создаем список с таймингами"""
        timing_list = re.findall('\d{2}:\d{2}:\d{2}', timing)



def theme_print ():
    """Функция для составления меню выбора"""
    global headers_list
    headers_list = timing_display[0].split('\n')
    point = 0
    for el in headers_list:
        number = re.match('\[', el)
        if number != None:
            point +=1
            print(point, el)
        else:
            continue


def theme_choise():
    """Выбор темы для прослушивание и начло воспроизведения"""
    flag = True
    while flag == True:
        try:
            choise = str(input("Нажмите цифру для выбора темы или [a]ll для прослушивания всего подкаста: "))

        except Exception:
            print("Ошибка - похоже вы ввели не тот символ.")
            continue
        choise_list = ["A", "a", "а", "А", "All", "all", "b"]
        if any(choise in s for s in choise_list):
            start_time = "00:00:00"
        else:
            choise = int(choise)
            choise -= 1
            start_time = timing_list[choise]
        flag = False
    print(start_time)
    os.system('mplayer -ss "{}" {}'.format(start_time, file_name_on_disk))


get_page_of_day(url)

page = open('index.html', 'r')
page_var = page.read()
soup = BeautifulSoup(page_var, 'html.parser')

soup = BeautifulSoup(page_var, 'lxml')
title_list = soup.find_all('h1', {'class': 'entry-title'})
name_dict = {}
podcast_name_list = []
podcast_link_list = []
dict_podcasts = {}
for item in title_list:
        podcast_name =  item.find('a').text
        podcast_link =  item.find('a').get('href')
        match = re.findall('Episode | episode', podcast_name)
        try:
            if match[0] == 'Episode' or 'episode':
                podcast_name_list.append(podcast_name)
                podcast_link_list.append(podcast_link)
        except IndexError:
            pass
dict_podcasts = dict(zip(podcast_name_list, podcast_link_list))


file_name_podcast = file_name(dict_podcasts)
url_podcast = podcast_link_list


on_hdd = lst_dir()

for el in file_name_podcast:
    if el in on_hdd:
        print("")
    else:
        try:
            url_podcast_end = url + el[0:12]
        except IndexError as err:
            print("Возможно статей стало больше 9999: ", err)
        file_name_podcast_end = el
        get_all_podcasts(url_podcast_end, file_name_podcast_end)


list_day_podcasts()

print("\n")
number_list = 1
pod_dict = {}
for el in file_name_podcast:
    print("[" + str(number_list) + "] ", el[0:12])
    pod_dict[number_list] = el
    number_list += 1

episode = int(input("\nВаш выбор: "))
choise_epis = pod_dict.get(episode)
print(choise_epis)

print("\n")
#Парсим и скачиваем выбранный эпизод
get_page_of_day(url)

page = open(choise_epis, 'r')

get_timing(page.read())
dicription_podcast = text_discription[0]
decore = textwrap.wrap(dicription_podcast, 80)
for el in decore:
    print(el)
print("\n")
# print(timing_list)
theme_print()
# print(headers_list)
page = open(choise_epis, 'r')
"""!!!!Остановился на выводе имери файла, вывести и передать функции для скачивания, запилить проверку на наличие файла"""
page_var2 = page.read()
podcast_link1 = get_mp3_from_page()
print("____" * 30)
file_name_on_disk = file_name_mp3(podcast_link1)
print(on_hdd)
if any(file_name_on_disk in s for s in on_hdd):
    theme_choise()
else:
    get_mp3_podcasts(podcast_link1, file_name_on_disk)
theme_choise()
