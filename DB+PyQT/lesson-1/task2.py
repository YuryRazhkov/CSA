'''2. Написать функцию host_range_ping() (возможности которой основаны на функции из примера1)
для перебора ip-адресов из заданного диапазона. Меняться должен только последний октет
каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.'''
import socket

from task1 import host_ping


def host_range_ping(ip_list, range_ip=24):
    list_ip_for_host_ping = []
    for ip in ip_list:
        try:
            for a in range(1, range_ip + 1):
                ip = ".".join(socket.gethostbyname(ip).split('.')[:3]) + '.' + str(a)  # получаем первые 3 октета и
                # добавляем четвертый по порядку в заданом диапазоне
                list_ip_for_host_ping.append(ip)
        except:
            list_ip_for_host_ping.append(ip)

    return host_ping(list_ip_for_host_ping)


if __name__ == "__main__":
    ip_list = ['192.168.100.1', '192.168.100.2', 'ya.ru', 'none.not', 'google.com']
    host_range_ping(ip_list=ip_list, range_ip=8)
