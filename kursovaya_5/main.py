

from utils import get_headhunter_data, create_database, save_data_to_database
from config import config


def main():

    list_top_company_ids = [999442, 4872201, 4949, 205152, 733, 5178281, 3388, 17222, 4138182, 42954]

    params = config()



    data = get_headhunter_data(list_top_company_ids)
    create_database('kursovaya5_db', params)
    save_data_to_database(data, 'kursovaya5_db', params)


if __name__ == '__main__':
    main()























