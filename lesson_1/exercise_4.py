words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    print(f'-------------Преобразование слова "{word}"------------')
    word_bytes = word.encode('utf-8')
    print('Преобразование из строки в байты\n', word_bytes)
    dec_word_bytes = word_bytes.decode('utf-8')
    print('Преобразование из байт в строку\n', dec_word_bytes)
    print('-----------------------------------------------------')