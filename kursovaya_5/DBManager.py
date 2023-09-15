

import psycopg2
from config import config



class DBManager:

    def __init__(self, word, database_name, params):
        self.word = word
        self.database_name = database_name
        self.params = params



    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT company_name, COUNT(*) 
                    FROM employers
                    JOIN vacancys USING (employer_id)
                    GROUP BY company_name
                """)
            result = cur.fetchall()
            for item in result:
                print(f"Название компании: {item[0].ljust(30)} Вакансий: {item[1]}")
        conn.commit()
        conn.close()


    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT company_name, vacancy_name, salary, vacancy_url
                            FROM employers
                            JOIN vacancys USING (employer_id)
                        """)
            result = cur.fetchall()
            for item in result:
                print(item)
        conn.commit()
        conn.close()


    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT AVG(salary) FROM vacancys
                        """)
            result = cur.fetchall()
            for item in result:
                print(f"Средняя зарплата: {round(item[0])}")
        conn.commit()
        conn.close()



    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT vacancy_name 
                            FROM vacancys
                            WHERE salary > (SELECT AVG(salary) FROM vacancys)
                        """)
            result = cur.fetchall()
            for item in result:
                print(f"Название вакансии: {item[0]}")
        conn.commit()
        conn.close()


    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова,
         например python"""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(f"""
                            SELECT vacancy_name
                            FROM vacancys
                            WHERE vacancy_name LIKE '%{self.word}%'
                        """)
            result = cur.fetchall()
            for item in result:
                print(f"Название вакансии: {item[0]}")
        conn.commit()
        conn.close()





params = config()

test = DBManager('Python','kursovaya5_db', params)


























