import requests
from bs4 import BeautifulSoup
from typing import Set


def parse_olx() -> Set[str]:
    olx_domen = 'https://www.olx.ua'
    main_url = olx_domen + '/d/uk/nedvizhimost/kiev/q-%D0%BD%D0%BE%D0%B2%D0%B0-%D0%B0%D0%BD%D0%B3%D0%BB%D1%96%D1%8F/' \
                           '?currency=UAH&search%5Bfilter_float_price:from%5D=9000&search%5B' \
                           'filter_float_price:to%5D=14000'
    apartment_url_class = 'css-1bbgabe'

    response = requests.get(main_url)
    soup = BeautifulSoup(response.text)
    apartment_urls = []
    for link_tag in soup.find_all('a', class_=apartment_url_class, href=True):
        apartment_url = olx_domen + link_tag.get('href')
        apartment_urls.append(apartment_url)

    return set(apartment_urls)


if __name__ == '__main__':
    parse_olx()

