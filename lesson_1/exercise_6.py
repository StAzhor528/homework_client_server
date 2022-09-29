from chardet import detect

with open('test_file.txt', 'w', encoding='utf-8') as f:
    f.write('сетевое программирование\nсокет\nдекоратор')

with open('test_file.txt', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']


with open('test_file.txt', encoding=encoding) as f:
    for line in f:
        print(line, end='')
