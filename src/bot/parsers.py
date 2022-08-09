import requests
from bs4 import BeautifulSoup
from typing import Set

olx_domen = 'https://www.olx.ua'
flatly_domen = 'https://flatfy.ua'


def parse_olx() -> Set[str]:
    main_url = olx_domen + '/d/uk/nedvizhimost/kiev/q-%D0%BD%D0%BE%D0%B2%D0%B0-%D0%B0%D0%BD%D0%B3%D0%BB%D1%96%D1%8F/' \
                           '?currency=UAH&search%5Bfilter_float_price:from%5D=9000&search%5B' \
                           'filter_float_price:to%5D=14000&page={page_number}'
    apartment_url_class = 'css-1bbgabe'

    apartment_urls = []
    for page_number in range(5):
        response = requests.get(main_url.format(page_number=page_number))
        soup = BeautifulSoup(response.text)
        for link_tag in soup.find_all('a', class_=apartment_url_class, href=True):
            apartment_url = olx_domen + link_tag.get('href')
            apartment_urls.append(apartment_url)
    return set(apartment_urls)


def parse_flatfy() -> Set[str]:
    main_url = flatly_domen + '/search?currency=UAH&geo_id=1&is_without_fee=false&page={page_number}' \
                              '&price_max=14000&price_sqm_currency=UAH&section_id=2&sort=insert_time&sub_geo_id=76987'

    apartment_url_class = 'realty-preview__content-link'

    apartment_urls = []
    for page_number in range(5):
        response = requests.get(main_url.format(page_number=page_number))
        soup = BeautifulSoup(response.text)
        for link_tag in soup.find_all('a', class_=apartment_url_class, href=True):
            apartment_url = flatly_domen + link_tag.get('href')
            apartment_urls.append(apartment_url)
    return set(apartment_urls)


def parse_url() -> Set[str]:
    olx_url = parse_olx()
    flatfy_urls = parse_flatfy()

    return olx_url.union(flatfy_urls)


