import os
import requests

from dotenv import load_dotenv

try:
    from . import constants
except ModuleNotFoundError:
    import constants


def load_data():
    url = f'{constants.PETANGLE_DATABASE_URL}products.json'
    return requests.get(url).json()


def main():
    load_dotenv()
    print(os.getenv('SLACK_URL'))
    return
    data = load_data()
    products_ids = list(data.keys())
    products_ids = list(map(lambda x: f'product/{x}', products_ids))

    resp = requests.post(
        constants.SITE_MAP_GENERATOR_URL,
        json={
            "url": constants.PETANGLE_URL,
            "endPoints": products_ids,
            "languages": ['cn', 'jp'],
        }
    )
    print(resp.json()['xml'])


if __name__ == '__main__':
    main()
