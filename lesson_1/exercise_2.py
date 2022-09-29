words = ['class', 'function', 'method']

for word in words:
    print('------------------------------------')
    print(f'преобразование в байты слова "{word}"')
    b_word = eval(f'b"{word}"')
    print('Содержимое преобразованного слова - ', b_word)
    print('Тип преобразованного слова - ', type(b_word))
    print('Длинна преобразованного слова - ', len(b_word))
    print('------------------------------------')

