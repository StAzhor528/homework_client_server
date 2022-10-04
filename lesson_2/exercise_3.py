import yaml

thing_list = ['Компьютер', 'Клавиатура', 'Мышь']
number = 1
thing_dict = {'Стол': '100₽',
              'Стул': '200€',
              'Диван': '0.03₿'}
data = {'thing_list': thing_list,
        'number': number,
        'thing_dict': thing_dict
        }

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=True)

with open('file.yaml', encoding='utf-8') as f:
    content = yaml.load(f, Loader=yaml.FullLoader)

if content == data:
    print('Данные полученые из файла file.yaml совпадают с исходными.')
else:
    print('Данные полученые из файла file.yaml не совпадают с исходными.')