import csv
from pprint import pprint

from chardet import detect
import re

files_list = ['data/info_1.txt', 'data/info_2.txt', 'data/info_3.txt']

def get_data(file_name):
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]

    for file in files_list:
        with open(file, 'rb') as f:
            f = f.read()
        encoding = detect(f)['encoding']

        with open(file, 'r', encoding=encoding) as file:
            file_data = file.read()
            os_prod = re.search('(?<=Изготовитель системы:)\s+(.*)', file_data)
            if os_prod:
                os_prod_list.append(os_prod.group(1))
            else:
                os_prod_list.append('no data')

            os_name = re.search('(?<=Название ОС:)\s+(.*)', file_data)
            if os_name:
                os_name_list.append(os_name.group(1))
            else:
                os_name_list.append('no data')

            os_code = re.search('(?<=Код продукта:)\s+(.*)', file_data)
            if os_code:
                os_code_list.append(os_code.group(1))
            else:
                os_code_list.append('no data')

            os_name = re.search('(?<=Тип системы:)\s+(.*)', file_data)
            if os_name:
                os_type_list.append(os_name.group(1))
            else:
                os_type_list.append('no data')

    main_data = [main_data]

    for i in range(len(os_prod_list)):
        main_data = main_data + [[(os_prod_list)[i]] + [(os_name_list)[i]] + [(os_code_list)[i]] + [(os_type_list)[i]]]

    with open(file_name, 'w', encoding='utf-8') as f_n:
        F_N_WRITER = csv.writer(f_n)
        F_N_WRITER.writerows(main_data)


def write_to_csv(file_name):
    get_data(file_name)

write_to_csv('test.csv')