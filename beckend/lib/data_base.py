"""
from: xHak2215
https://github.com/xHak2215/MAX_idi_na_hui_messenger/blob/main/data_bese.py
GNU GENERAL PUBLIC LICENSE
"""

import sqlite3
import traceback
import json
import time

from lib.config_init import logger, SECRET_KEY
from lib.tokenizer import creat_refresh_token, verify_refresh_token

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
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        works TEXT,
        classU INTEGER,
        refresh_token TEXT NOT NULL
    )
    ''')
    
    # Создаем индекс (если он еще не существует)
    cursor.execute('CREATE INDEX IF NOT EXISTS user_id_index ON Users (id)')
    return connection, cursor

def update_user(refresh_token:str, relust:dict):
    """**update data bese**
    
    Args:
        refresh_token (_str_): токен пользователя
        relust (dict): словарь где ключ это название столбца а содержимое данные

    Returns:
        None:при ошибке
    """
    # Создаем подключение к базе данных
    connection = sqlite3.connect('data_base.db', timeout=10)
    cursor = connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")

    # Формируем запрос для обновления
    query = "UPDATE Users SET "
    params = []
    updates = []
    
    if relust is not None:
        for key in list(relust.keys()):
            updates.append(key+"= ?")
            params.append(str(relust[key]))
    
    # Проверяем, были ли добавлены параметры
    if not updates:
        connection.close()
        #logger.warning("update_user Нет параметров для обновления.")
        return None
    
    query += ", ".join(updates)
    query += " WHERE refresh_token = ?"
    params.append(refresh_token)
    
    try:
        cursor.execute(query, params)
        connection.commit()
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return None
    finally:
        connection.close()

def register(name:str, surname:str, email:str, password:str, role:str, works:str, classU:int, devise_id:str) -> dict:
    """
    Args:
        name(str): имя пользователя
        surname(str): фамилия пользователя
        email(str): эл. почта пользователя
        password(str): пароль пользователя 
        role(str): роль ученик/учитель
        works(str): на будущее
        classU(int): класс (для ученика)
    Return:
        dict: стандартный ответ от базы данных (см. doc/DATABASE.md)
    """
    try:
        connection, cursor = init_users()
    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    try:    
        # Проверяем, существует ли пользователь с данными name, surname и email
        cursor.execute('SELECT * FROM Users WHERE name = ? AND surname = ? AND email = ?', (name, surname, email))
        result = cursor.fetchone()

        if result is None:
            refresh_token = json.dumps({devise_id: creat_refresh_token(name, surname, email, SECRET_KEY)})

            cursor.execute('INSERT INTO Users (name, surname, email, password, role, works, classU, refresh_token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
            (name, surname, email, password, role, works, classU, refresh_token))

            connection.commit()
            connection.close()
            # "password":password, пароль хоть он и захеширован не отповяю
            return {"is_ok": True, "error_code":None, "details": None, "data": 
            {"name":name, "surname":surname, "email":email, "role":role, "works": works, "class":classU, "refresh_token":refresh_token}}
        else:
            connection.commit()
            connection.close()
            return {"is_ok": False, "error_code":403, "details":"такой пользователь уже существует", "data":None}

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()

def get_data_for_token(token:str, time:float, devise_id:str):
    try:
        connection, cursor = init_users()
    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    try:
        cursor.execute('SELECT * FROM Users WHERE token = ?', (token))
        result = cursor.fetchone()

        if result:
            print(token, result[1], result[2], result[3], SECRET_KEY, time)
            if verify_refresh_token(token, result[1], result[2], result[3], SECRET_KEY, time):

                logger.info(f"token {result[1]} {result[2]} verefy")
                if time - time.time() < 157784808: # если прошло менее 6 месяцев и срок токена не истек
                    refresh_token = json.dumps(creat_refresh_token(result[1], result[2], result[3], SECRET_KEY))
                    update_user(token, {devise_id: {"refresh_token": refresh_token}})

                    return {"is_ok": True, "error_code":None, "details": None, "data": 
                    {"name":result[1], "surname":result[2], "email":result[3], "role":result[5], "works": result[6], "class":result[7], "refresh_token":refresh_token}}
                else:
                    return {"is_ok": False, "error_code":401, "details": f"срок авторизации истек", "data": None}
            else:
                return {"is_ok": False, "error_code":401, "details": f"не подтвержденная авторизация, ошибка безопасности", "data": None}
        else:
            return {"is_ok": False, "error_code":401, "details": f"не подтвержденная авторизация", "data": None}

    except Exception as e:
        logger.error(f'Ошибка в операции с базой данных: {e}\n{traceback.format_exc()}')
        connection.close()
        return {"is_ok": False, "error_code":500, "details": f"server error: {e}", "data": None}
    finally:
        # Закрываем соединение
        connection.close()