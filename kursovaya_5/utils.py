from typing import Any
import requests
import psycopg2

def get_headhunter_data(company_ids: list[int]) -> list[dict[str,Any]]:
    """Получение данных о вакансии и работодателе с помощью HeadHunter Api"""

    data = []


    for company_id in company_ids:
        vacancys_data = []
        params = {
            'employer_id': company_id,
            'page': 1,
            'per_page': 10,
            "only_with_salary": True
        }
        api = requests.get('https://api.hh.ru/vacancies', params=params)

        dict_with_info = api.json()



        for i in dict_with_info['items']:
            vacancys_data.append(i)


        data.append({
            'company_name':dict_with_info['items'][0]['employer']['name'],
            'vacancys':vacancys_data
        })

    return data



def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц"""


    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancys (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR NOT NULL,
                salary INT,
                vacancy_url TEXT
            )
        """)


    conn.commit()
    conn.close()




def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о вакансиях и работодателях в базу данных"""


    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employers in data:
            company_name = employers['company_name']

            vacancys = employers['vacancys']


            cur.execute(
                """
                INSERT INTO employers (company_name)
                VALUES (%s)
                RETURNING employer_id
                """,
                ([company_name])
            )

            employer_id = cur.fetchone()[0]


            for employer in vacancys:

                vacancy_name = employer['name']

                vacancy_url = employer['alternate_url']
                if employer['salary']['from'] == None:
                    salary = employer['salary']['to']
                elif employer['salary']['to'] == None:
                    salary = employer['salary']['from']
                else:
                    salary = employer['salary']['from']

                cur.execute(
                    """
                    INSERT INTO vacancys (employer_id, vacancy_name, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (employer_id, vacancy_name, salary,
                     vacancy_url)
                )






    conn.commit()
    conn.close()









