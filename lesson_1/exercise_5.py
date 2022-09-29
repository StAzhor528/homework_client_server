import locale
import subprocess
import platform

param = '-n' if platform.system().lower() == 'windows' else '-c'
args_yandex = ['ping', param, '2', 'yandex.ru']
args_youtube = ['ping', param, '2', 'youtube.com']

print('-------------Пинг yandex.ru----------')
with subprocess.Popen(args_yandex, stdout=subprocess.PIPE) as process:
    for line in process.stdout:
        default_encoding = locale.getpreferredencoding()
        line = line.decode(default_encoding).encode('utf-8')
        print(line.decode('utf-8'), end='')
    print('--------------------------')
print('-------------Пинг youtube.com----------')
with subprocess.Popen(args_youtube, stdout=subprocess.PIPE) as process:
    for line in process.stdout:
        default_encoding = locale.getpreferredencoding()
        line = line.decode(default_encoding).encode('utf-8')
        print(line.decode('utf-8'), end='')
    print('--------------------------')