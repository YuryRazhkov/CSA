"""1.

Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().
 (Внимание! Аргументом сабпроцеса должен быть список, а не строка!!!
Для уменьшения времени работы скрипта при проверке нескольких ip-адресов, решение необходимо выполнить
с помощью потоков)"""
import ipaddress
import platform
import socket
import subprocess
import time
from threading import Thread

ip_dict = {  # На лекции было сказано, что надо формировать словарь адресов с ключами "доступен" и "недоступен"
    'Узел доступен': [],
    'Узел недоступен': [],
}


def ping_ip(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '4', ip.__str__()]
    reply = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if reply.wait() == 0:
        ip_dict['Узел доступен'].append(ip)
    else:
        ip_dict['Узел недоступен'].append(ip)


def host_ping(ip_list):
    list_ip_subnet = []
    for i in ip_list:  # понимаю, что накручено, но как по другому впихнуть сюда ip_address() не придумал
        try:
            list_ip_subnet.append(ipaddress.ip_address(socket.gethostbyname(i)))
        except:  # но так мы экономим на том, что не пингуем заведомо ложные ip
            ip_dict['Узел недоступен'].append(i)
    threads = []
    for ip in list_ip_subnet:
        THR = Thread(target=ping_ip, args=(ip,))
        THR.start()
        threads.append(THR)

    for thread in threads:
        thread.join()

    return ip_dict


def ping_queue(ip_list):  # проверим  на сколько быстрее справятся потоки

    list_ip_subnet = []
    for i in ip_list:  # понимаю, что накручено, но как по другому впихнуть сюда ip_address() не придумал
        try:
            list_ip_subnet.append(ipaddress.ip_address(socket.gethostbyname(i)))
        except:  # но но так мы экономим на том, что не пингуем заведомо ложные адреса
            ip_dict['Узел недоступен'].append(i)

    for ip in list_ip_subnet:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        args = ['ping', param, '4', ip.__str__()]
        reply = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if reply.wait() == 0:
            ip_dict['Узел доступен'].append(ip.__str__())
        else:
            ip_dict['Узел недоступен'].append(ip.__str__())

    return ip_dict


if __name__ == "__main__":
    ip_list = ['192.168.100.1', '192.168.100.2', 'ya.ru', 'none.not', 'google.com']

    start = time.time()
    print(host_ping(ip_list))
    stop = time.time()
    time_host_ping = stop - start
    print('elapsed time', time_host_ping)

    start = time.time()
    print(ping_queue(ip_list))
    stop = time.time()
    time_ping_queue = stop - start
    print('elapsed time', ('elapsed time', time_ping_queue))
    print(f'threads took {time_ping_queue / time_host_ping} times less time to complete this task')
