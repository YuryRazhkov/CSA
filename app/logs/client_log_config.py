import sys
import os

import logging.handlers


sys.path.append('../')

# Создание именованного логгера;
LOGGER = logging.getLogger('clientapp')

# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Логирование должно производиться в лог-файл;
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

FILE_HANDLER = logging.FileHandler(PATH, encoding='utf-8')

FILE_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.INFO)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
