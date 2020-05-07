import requests
from lxml import html
import schedule
import time
from datetime import datetime
import os

def scheduler():
    print('turn on')
    while True:
        date = str(datetime.now().time()).split(':')
        date[2] = date[2].split('.')
        if (date[0] == '16') and (date[1] == '11') and (date[2][0] == '01'):
            print(date)
            get_data()
            print('done')
            break
    print('turn off')
    scheduler()


def get_data():
    url = 'https://meduza.io/feature/2020/04/17/koronavirus-v-rossii-poslednie-dannye'
    data = requests.get(url)
    with open('table.html', 'w', encoding='utf-8') as output_file:
        output_file.write(data.text)
    table_html = open('table.html', 'r', encoding='utf-8')
    output = open('data.txt', 'w')
    text = table_html.read()
    tree = html.fromstring(text)
    table_rows = tree.xpath('//div[@class = "Table-row"]')
    count_row = 0
    for table_row in table_rows:
        count_row += 1
        for elem in table_row:
            if count_row == 87:
                text_inside = elem.xpath('.//strong')
            else:
                text_inside = elem.xpath('.//p')
            if text_inside:
                col = text_inside[0].text
                if col is None:
                    src = elem.xpath('.//strong')
                    col = src[0].text
                col = col.replace(chr(160), '')
                col = col + ' '
                if count_row != 0:
                    output.write(col)
        output.write('\n')
    output.close()
    table_html.close()
    os.remove('table.html')


def get_stat_by_name(name):
    def str_comparison(str1, str2):
        if len(str1) != len(str2):
            return False
        else:
            str1 = str1.lower()
            str2 = str2.lower()
            i = len(str1) - 1
            while i != 0:
                if str1 != str2:
                    return False
                else:
                    return True

    # modify name for work
    if name.isdigit(): return False
    output = open('data.txt', 'r')
    for line in output.readlines():
        current_line = line.split(' ')
        current_size = len(current_line)
        if current_size == 7:
            current_line[1] = current_line[1] + ' ' + current_line[2]
        if current_size == 8:
            current_line[1] = current_line[1] + ' ' + current_line[2] + ' ' + current_line[3]
        comp_line = current_line[1]
        if str_comparison(name, comp_line):
            size = len(current_line)
            output = []
            output.append('Место по заболевшим: ' + current_line[0])
            output.append('Заболело: ' + current_line[size - 4])
            output.append('Умерли: ' + current_line[size - 3])
            output.append('Вылечилось: ' + current_line[size - 2])
            return output
    return False

# print('Введите строку')
# s = input()
# if get_stat_by_name(s):
#     print(get_stat_by_name(s))
# else:
#     print('Неверный ввод')
