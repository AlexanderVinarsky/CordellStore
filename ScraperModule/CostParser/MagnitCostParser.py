import json
from types import SimpleNamespace

import requests

from ScraperModule.CostParser.Objects.Goods import Goods

headers = {
    'authority': 'web-gateway.middle-api.magnit.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://magnit.ru',
    'referer': 'https://magnit.ru/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'x-app-version': '0.1.0',
    'x-client-name': 'magnit',
    'x-device-id': 'x5glri6mny',
    'x-device-platform': 'Web',
    'x-device-tag': 'disabled',
    'x-platform-version': 'window.navigator.userAgent',
}


def parse_products(magnit_store):
    json_data = {
        'categoryIDs': [],
        'includeForAdults': True,
        'onlyDiscount': False,
        'order': 'desc',
        'pagination': {
            'number': 1,
            'size': 36,
        },
        'shopType': '1',
        'sortBy': 'price',
        'storeCodes': [
            magnit_store.code,
        ],
    }

    response = json.loads(requests.post('https://web-gateway.middle-api.magnit.ru/v3/goods', headers=headers,
                                        json=json_data).text, object_hook=lambda d: SimpleNamespace(**d))

    goods_list = []
    for goods in response.goods:
        goods_list.append(Goods(goods=goods))

    return goods_list

