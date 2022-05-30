'''3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
Reachable
10.0.0.1
10.0.0.2

Unreachable
10.0.0.3
10.0.0.4
'''
from tabulate import tabulate

from task2 import host_range_ping


def host_range_ping_tab(ip_list):
    resulnt_of_ping = host_range_ping(ip_list)
    print(tabulate(resulnt_of_ping, headers='keys', tablefmt="pipe", stralign="left"))


if __name__ == "__main__":
    ip_list = ['192.168.100.1', '127.0.0.1', 'ya.ru', 'none.not', 'google.com']
    host_range_ping_tab(ip_list)
