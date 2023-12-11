import psycopg2

from func_db import connect_config_db, create_db, save_data_to_database
from parse_api_hh import get_vacancies
from class_DBManager import DBManager

if __name__ == '__main__':
    
    db_name = 'company_and_vacancies'  # Задаем имя базе данных
    params = connect_config_db('database.ini')  # Файл с конфигурацией подключения
    
    create_db(params, db_name)  # Создаем базу данных
    vacancies_list = get_vacancies()  # Получаем список вакансий
    save_data_to_database(vacancies_list, db_name, params)  # Заполняем таблицы базы данных
    connection = psycopg2.connect(dbname=db_name, **params)  # Подключаемся к базе данных
    
    with connection as conn:
        with conn.cursor() as cur:
            db_manager = DBManager(cur)
            
            while True:
                print("\nВыберете из списка  действие:\n"
                      "\n1 - Вывести весь список компаний с указанием "
                      "кол-ва найденных вакансий (по убыванию)\n"
                      "2 - Вывести весь список вакансий\n"
                      "3 - Вывести среднюю ЗП по всем вакансиям\n"
                      "4 - Вывести список вакансий у которых ЗП "
                      "выше средней по всем вакансия\n"
                      "5 - Вывести список всех вакансий по ключевому "
                      "слову в названии вакансии\n"
                      "0 - Выйти")
                user_func_input = input("> ")
                if user_func_input == "0":
                    print("Goodbye my friend")
                    break
                
                if user_func_input == "1":
                    companies = db_manager.get_companies_and_vacancies_count()
                    for company in companies:
                        print(f"Компания: {company[0]}\nНайдено вакансий: {company[1]}\n")
                
                if user_func_input == "2":
                    vacancies = db_manager.get_all_vacancies()
                    for vacancy in vacancies:
                        print(f"Компания: {vacancy[0]}\nВакансия: {vacancy[1]}\n"
                              f"Зарплата от: {vacancy[2]}\nЗарплата до: {vacancy[3]}\n"
                              f"Ссылка: {vacancy[4]}\n")
                
                if user_func_input == "3":
                    print(f"{round(db_manager.get_avg_salary()[0][0])} руб.\n")
                
                if user_func_input == "4":
                    valid_vac = db_manager.get_vacancies_with_higher_salary()
                    for vac in valid_vac:
                        print(f"Компания: {vac[5]}\nВакансия: {vac[1]}\nЗарплата: {vac[3]}\nСсылка: {vac[4]}\n")
                
                if user_func_input == "5":
                    while True:
                        word_input = input("Введите название вакансии для поиска"
                                           "или 0 для выхода:\n> ")
                        vacancy_list = db_manager.get_vacancies_with_keyword(word_input)
                        if word_input == "0":
                            break
                        if len(vacancy_list) == 0:
                            print("Таких вакансий нет \nПопробуйте себя в чем то другом!\n")
                        else:
                            for vac in vacancy_list:
                                print(f"Вакансия: {vac[2]}\nЗарплата от: {vac[3]}\n"
                                      f"Зарплата до: {vac[4]}\nСсылка: {vac[5]}")
                                print()
                            break
