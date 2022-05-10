import sys
import os

import logging.handlers


sys.path.append('../')

# Создание именованного логгера;
LOGGER = logging.getLogger('serverapp')

# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Логирование должно производиться в лог-файл;
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')
LOG_FILE = logging.FileHandler(PATH, encoding='utf-8')
LOG_FILE.setFormatter(FORMATTER)

LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(logging.INFO)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
