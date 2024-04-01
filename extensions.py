import requests
import json
from config import CURRENCY_API_URL, CURRENCY_API_KEY, CURRENCIES


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        base = base.lower()
        quote = quote.lower()

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            base_ticker = CURRENCIES[base]
            quote_ticker = CURRENCIES[quote]
        except KeyError as e:
            raise APIException(f'Невозможно найти валюту: {e}')

        try:
            response = requests.get(
                f'{CURRENCY_API_URL}?fsym={base_ticker}&tsyms={quote_ticker}&api_key={CURRENCY_API_KEY}')
            if response.status_code != 200:
                raise APIException('Ошибка при выполнении запроса к API.')

            resp_json = json.loads(response.content)
            if quote_ticker in resp_json:
                return round(resp_json[quote_ticker] * float(amount), 2)
            else:
                raise APIException(f'Ошибка при запросе курса валюты {base} в {quote}.')
        except ValueError:
            raise APIException('Некорректное количество валюты.')

    @staticmethod
    def get_available_currencies():
        return list(CURRENCIES.keys())
