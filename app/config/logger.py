__all__ = ["setup_log"]

import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_log(name):
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d - %(message)s'
    )
    
    # Обработчик для файла (с ротацией)
    file_handler = RotatingFileHandler(
        'app/logs/app.log', maxBytes=1_000_000, backupCount=5, encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    console_handler.encoding = 'utf-8'
    
    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger