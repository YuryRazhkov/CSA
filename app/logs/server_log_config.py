import logging.handlers
import os
import sys

sys.path.append('../')

# Создание именованного логгера;
LOGGER = logging.getLogger('serverapp')

# Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Логирование должно производиться в лог-файл;
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D', backupCount=5)
LOG_FILE.setFormatter(FORMATTER)

LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
