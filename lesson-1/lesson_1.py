import platform
import subprocess

import chardet
from chardet import detect

'''1. Каждое из слов "разработка", "сокет", "декоратор" представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных.'''

print('\ntask 1')
smpl_list = ['разработка', 'сокет', 'декоратор']

for word in smpl_list:
    print(word, type(word))

smpl_list_unicode = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                     '\u0441\u043e\u043a\u0435\u0442',
                     '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for word in smpl_list_unicode:
    print(word, type(word))

print('\ntask 2')
'''2. Каждое из слов "class", "function", "method" записать в байтовом типе. Сделать это необходимо в автоматическом,
а не ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя
методы encode, decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.'''

smpl_list_bite = ['class', 'function', 'method']

for word in smpl_list_bite:
    word = eval(f"b'{word}'")
    print(word, type(word), len(word))

print('\ntask 3')
'''3. Определить, какие из слов "attribute", "класс", "функция", "type" невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.'''

smpl_list_nobyte = ['attribute', 'класс', 'функция', 'type', '25', '--']

for word in smpl_list_nobyte:
    try:
        print(word.encode('ascii'), type(word))
    except UnicodeEncodeError:
        print(f'слово "{word}" невозможно записать в байтовом типе')

print('\ntask 4')
'''4. Преобразовать слова "разработка", "администрирование", "protocol", "standard" из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).'''

smpl_list_encoding = ["разработка", "администрирование", "protocol", "standard"]

for word in smpl_list_encoding:
    word_bite = word.encode('utf-8')
    word_str = bytes.decode(word_bite, encoding='utf-8')
    print(word_bite, type(word_bite), word_str, type(word_str))

'''5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
в строковый тип на кириллице.'''

urls = ['yandex.ru', 'youtube.com']
param = '-n' if platform.system().lower() == 'windows' else '-c'

for url in urls:
    process = subprocess.Popen(('ping', param, '4', url), stdout=subprocess.PIPE)
    print(process)

    for line in process.stdout:
        result = chardet.detect(line)
        print('result = ', result)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))

'''6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», 
«сокет», «декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из того, 
что перед нами файл в неизвестной кодировке. 
Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.'''

smpl_list_file = ['сетевое программирование', 'сокет', 'декоратор']

with open('test_file.txt', 'w', encoding='utf-8') as f:
    for word in smpl_list_file:
        f.write(word + '\n')

with open('test_file.txt', 'rb') as f:
    f = f.read()
encoding = detect(f)['encoding']

with open('test_file.txt', 'r', encoding=encoding) as f:
    f = f.read()
print(f)
