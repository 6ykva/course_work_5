import requests

from class_DBManager import json_load

# id компаний
companies_id = json_load('employers.json')
companies_id_list = list(companies_id.values())


def get_vacancies():
    """
    Получение всех вакансий компаний
    """
    vacancies_list = []
    hh_api = 'https://api.hh.ru/vacancies'
    
    for comp_id in range(len(companies_id_list)):
        params = {
            'employer_id': companies_id_list[comp_id],
            'area': 1,
            'per_page': 100,
        }
        response = requests.get(hh_api, params=params)
        vacancies = response.json()
        for vacancy in vacancies['items']:
            if vacancy.get('salary') is None:
                vacancies_list.append(vacancy)
                
            else:
                vacancies_list.append(vacancy)
    
    return vacancies_list
