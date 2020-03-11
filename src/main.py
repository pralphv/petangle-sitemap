import logging
import requests

from flask import Flask, make_response

try:
    from . import constants
except (ModuleNotFoundError, ImportError):
    import constants

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s: %(message)s")

app = Flask(__name__)


def load_data():
    logging.debug('Fetching data from Firebase')
    url = f'{constants.PETANGLE_DATABASE_URL}products.json'
    data = requests.get(url).json()
    logging.debug('Successfully fetched data from Firebase')
    return data


def process_data(products_ids):
    logging.debug('Sending request to sitemap-generator-heroku')
    resp = requests.post(
        constants.SITE_MAP_GENERATOR_URL,
        json={
            "url": constants.PETANGLE_URL,
            "endPoints": products_ids,
            "languages": ['cn', 'jp'],
        }
    )
    logging.debug('Successfully received response from sitemap-generator-heroku')
    return resp.json()['xml']


@app.route('/sitemap.xml')
def run():
    logging.debug("Starting script to update Petangle's sitemap")
    data = load_data()
    products_ids = list(data.keys())
    products_ids = list(map(lambda x: f'product/{x}', products_ids))
    data = process_data(products_ids)
    logging.debug("Returning response")
    res = make_response(data, 200)
    res.headers["Content-Type"] = "application/xml"
    logging.debug("Successfully responded")
    return res


if __name__ == '__main__':
    app.run(debug=False)
