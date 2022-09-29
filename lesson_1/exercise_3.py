words = ['attribute', 'класс', 'функция', 'type']

for word in words:
    try:
        eval(f'b"{word}"')
    except SyntaxError:
        print(f'Слово "{word}" невозможно записать в байтовом типе')
