from configparser import ConfigParser

import psycopg2

from class_DBManager import json_load

company_list_id = json_load('employers.json')


def connect_config_db(filename):
    """
    :param filename: данные из database.ini
    :return: параметры подключения
    """
    
    parser = ConfigParser()
    parser.read(filename)
    db_params = dict(parser.items('postgresql'))
    
    return db_params


def create_db(params, db_name) -> None:
    """
    Создаем базу данных с таблицами
    :param params: параметры подключения
    :param db_name: имя базы данных
    """
    
    print("Создается база данных")
    
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")
    
    cur.close()
    conn.close()
    
    print("База данных создана")
    
    print("Создаются таблицы с компаниями и вакансиями")
    
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("\n"
                    "    CREATE TABLE company (\n"
                    "                 company_id int PRIMARY KEY,\n"
                    "                 company_name varchar(50) UNIQUE\n"
                    ")\n")
    
    with conn.cursor() as cur:
        cur.execute("\n"
                    "CREATE TABLE vacancies (\n"
                    "vacancy_id int PRIMARY KEY,\n"
                    "company_name varchar(50) REFERENCES company(company_name) NOT NULL,\n"
                    "vacancy_name varchar(100) NOT NULL,\n"
                    "vacancy_salary_from int,\n"
                    "vacancy_salary_to int,\n"
                    "vacancy_url text\n"
                    ")\n")
    
    conn.commit()
    conn.close()
    
    print("Создание таблиц завершено!\n")


def save_data_to_database(vacancies_list, db_name, params):
    """
    Заполнение таблиц
    """
    
    conn = psycopg2.connect(dbname=db_name, **params)  # создание подключения к БД
    with conn.cursor() as cur:
        for name in company_list_id:
            cur.execute(f"INSERT INTO company VALUES (%s, %s)",
                        (int(company_list_id[name]), name))
        
        for item in vacancies_list:
            if item.get('salary') is None:
                cur.execute(f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                            (int(item['id']), item['employer']['name'], item['name'],
                             '0', '0', item['alternate_url']))
            else:
                cur.execute(f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                            (int(item['id']), item['employer']['name'], item['name'],
                             item['salary']['from'], item['salary']['to'], item['alternate_url']))
    
    conn.commit()
    conn.close()
    
    print("Таблицы заполнены!")
