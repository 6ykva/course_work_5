import json


class DBManager:
    """
    Класс для получения информации из Базы Данных
    """
    
    def __init__(self, cursor):
        self.cursor = cursor
    
    def get_companies_and_vacancies_count(self):
        """
        Получение списка компаний и кол-ва вакансий
        """
        self.cursor.execute("SELECT company_name, COUNT(*) AS vacancies_count "
                            "FROM vacancies "
                            "INNER JOIN company USING(company_name) "
                            "GROUP BY company_name "
                            "ORDER BY vacancies_count DESC")
        
        return self.cursor.fetchall()
    
    def get_all_vacancies(self):
        """
        Получение списка всех вакансий
        """
        self.cursor.execute("SELECT company_name, vacancy_name, vacancy_salary_from, "
                            "vacancy_salary_to, vacancy_url "
                            "FROM vacancies "
                            "INNER JOIN company USING(company_name)")
        
        return self.cursor.fetchall()
    
    def get_avg_salary(self):
        """
        Получение средней зарплаты по всем найденным вакансиям
        """
        self.cursor.execute("SELECT AVG(vacancy_salary_to) FROM vacancies WHERE vacancy_salary_to > 0")
        
        return self.cursor.fetchall()
    
    def get_vacancies_with_higher_salary(self):
        """
        Получение списка вакансий с ЗП больше чем средняя "от" и средняя "до" по всем вакансиям
        """
        self.cursor.execute("SELECT vacancy_id, vacancy_name, company_id, "
                            "vacancy_salary_to, vacancy_url, company_name FROM vacancies "
                            "INNER JOIN company USING(company_name) "
                            "WHERE vacancy_name IS NOT NULL "
                            "GROUP BY vacancy_id, vacancy_name, company_id, "
                            "vacancy_salary_to, vacancy_url "
                            "HAVING vacancy_salary_to > (SELECT AVG(vacancy_salary_to) "
                            "FROM vacancies WHERE vacancy_salary_to > 0) ")
        
        return self.cursor.fetchall()
    
    def get_vacancies_with_keyword(self, word):
        """
        Получение списка вакансий по ключевому слову
        """
        self.cursor.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{word}%'")
        return self.cursor.fetchall()


def json_load(file_json):
    """
    Загружаем json файл
    """
    with open(file_json, "r", encoding="utf-8") as cat_file:
        data = json.load(cat_file)
        return data
