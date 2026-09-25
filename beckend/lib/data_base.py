"""
from: xHak2215
https://github.com/xHak2215/MAX_idi_na_hui_messenger/blob/main/data_bese.py
GNU GENERAL PUBLIC LICENSE
"""

import sqlite3
import traceback
import json

from logse import *
logger = logse()


def init_users():
    """
    **отвечает за создание подключения и инициализацию табицы, сталбцов**

    Returns:
        tuple: connect, cursor
    """

    # Создаем подключение к базе данных
    connection = sqlite3.connect('data_base.db', timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Создаем таблицу (если она еще не существует)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        status TEXT NOT NULL,
        works TEXT
    )
    ''')
    
    # Создаем индекс (если он еще не существует)
    cursor.execute('CREATE INDEX IF NOT EXISTS user_id_index ON Users (id)')
    return connection, cursor

def register(name:str, email:str, password:str, status:str) -> dict:
    """
    Args:
        name(str): имя пользователя
        email(str): эл. почта пользователя
        password(str): пароль пользователя 
        status(str): статус ученик/учитель
    Return:
        dict: стандартный ответ от базы данных (см. doc/DATABASE.md)
    """
    try:
        connection, cursor = init_users()
    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    try:    
        # Проверяем, существует ли пользователь с данными login и password
        cursor.execute('SELECT * FROM Users WHERE name = ?  AND email = ?', (name, email))
        result = cursor.fetchone()

        if result is  None:
            cursor.execute('INSERT INTO Users (name, email, password, status) VALUES (?, ?, ?, ?)', (name, email, password, status))
            connection.commit()
            connection.close()
            return {"is_ok": True, "error_code":None, "details": None, "data": {"name":name, "email":email, "password":password, "status":status}}
        else:
            connection.commit()
            connection.close()
            return {"is_ok": False, "error_code":403, "details":"такой пользователь уже существует", "data":None}

    except Exception as e:a
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()