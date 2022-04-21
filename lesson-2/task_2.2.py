''' 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.'''
import json


def write_order_to_json(**kwargs):
    with open('data/orders.json', encoding='utf-8') as f:
        data = json.loads(f.read())
        data['orders'].append(kwargs)

    with open('data/orders.json', "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, separators=(',', ': '), ensure_ascii=False)

write_order_to_json(item='lovt', quantity=22, price=5200, buyer='Iva2n', date='2022-03-20')
