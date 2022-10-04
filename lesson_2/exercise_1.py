import os
import re
import csv
from chardet import detect


def get_data(txt_files):
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'], ]
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for txt_file in txt_files:
        with open(txt_file, 'rb') as f:
            content = f.read()
        encoding = detect(content)['encoding']

        with open(txt_file, encoding=encoding) as f:
            content = f.read()
            content_without_space = content.replace(' ', '')
            os_manufacturer = re.search(r'ИзготовительОС:\S+', content_without_space)
            os_name = re.search(r'НазваниеОС:\S+', content_without_space)
            product_code = re.search(r'Кодпродукта:\S+', content_without_space)
            type_of_system = re.search(r'Типсистемы:\S+', content_without_space)
            os_prod_list.append(os_manufacturer[0].split(':')[-1])
            os_name_list.append(os_name[0].split(':')[-1])
            os_code_list.append(product_code[0].split(':')[-1])
            os_type_list.append(type_of_system[0].split(':')[-1])
    for i in range(len(main_data[0]) - 1):
        os_data_list = [os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]]
        main_data.append(os_data_list)
    return main_data


def write_to_csv(csv_file):
    if not isinstance(csv_file, str):
        return print('Неверный тип исходных данных')
    if not csv_file.split('.')[-1] == 'csv':
        return print('Файл, который вы хотите создать должен иметь расширение .csv')
    files_in_work_dir = os.listdir()
    txt_files = []
    for file in files_in_work_dir:
        if file.split('.')[-1] == 'txt':
            txt_files.append(file)
    data = get_data(txt_files)
    print(data)
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        f_writen = csv.writer(f)
        f_writen.writerows(data)


write_to_csv('test.csv')

with open('test.csv', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']

with open('test.csv', encoding=encoding) as f:
    lines = f.read()
    print(lines)

