from __future__ import annotations

import httpx
import requests

from scrapper.objects.product import Product
from scrapper.objects.store import Store


class MagnitStore(Store):
    def __init__(self, store: dict) -> None:
        super().__init__("Магнит", store['latitude'], store['longitude'])

        self.code: int = store['code']
        for current_good in self._parse_products(256):
            self.storage.add(current_good)

    def _parse_products(self, goods_count: int) -> list[Product]:
        cookies = {
            '_ga': 'GA1.1.860917445.1730309330',
            '_ym_uid': '1730309331268901850',
            '_ym_d': '1730309331',
            '_ym_isad': '1',
            'nmg_udi': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'x_device_id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'PHPSESSID': 'isk7mh3ikbsscvta83ecgev03k',
            'nmg_sp': 'Y',
            '_ga_L0N0B74HJP': 'GS1.1.1730311671.2.1.1730311671.60.0.0',
            'shopCode': f'{self.code}',
            'x_shop_type': 'MM',
            'nmg_sid': '12382',
            'shopId': '12382',
        }

        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://magnit.ru',
            'Referer': 'https://magnit.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-app-version': '7.0.0',
            'x-client-name': 'magnit',
            'x-device-id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'x-device-platform': 'Web',
            'x-device-tag': 'disabled',
            'x-new-magnit': 'true',
            'x-platform-version': 'Windows Chrome 132',
        }

        goods_list = []
        for i in range(goods_count // 30):
            json_data = {
                'sort': {
                    'order': 'desc',
                    'type': 'popularity',
                },
                'pagination': {
                    'limit': 30,
                    'offset': i,
                },
                'categories': [ ],
                'includeAdultGoods': True,
                'storeCode': f'{self.code}',
                'storeType': '1',
                'catalogType': '1',
            }

            response = requests.post('https://magnit.ru/webgate/v2/goods/search', cookies=cookies, headers=headers, json=json_data)
            if response.status_code == 200:
                goods = response.json().get('items', [])
                try:
                    for prod in goods:
                        goods_list.append(Product(goods=prod))
                except Exception as e:
                    pass

        return goods_list

    @staticmethod
    async def load_magnit_stores(
        place: str = None, lon: float = None, lat: float = None, store_count: int = 50, search_radius: int = 5
    ) -> list[MagnitStore]:
        
        stores = []
        if place is not None:
            for store in Store.parse_near_stores(place)[:store_count]:
                stores.extend(await MagnitStore.get_near_magnit_stores(store.y_coordinate, store.x_coordinate, search_radius, 1))
        else:
            stores.extend(await MagnitStore.get_near_magnit_stores(lat, lon, search_radius, 1))

        return stores

    @staticmethod
    async def get_near_magnit_stores(lat: float, lon: float, radius: float = .02, count: int = 1) -> list[MagnitStore]:
        cookies = {
            '_ga': 'GA1.1.860917445.1730309330',
            '_ym_uid': '1730309331268901850',
            '_ym_d': '1730309331',
            '_ym_isad': '1',
            '_ym_visorc': 'b',
            'nmg_udi': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'x_device_id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'shopCode': '992301',
            'x_shop_type': 'ME',
            'PHPSESSID': 'isk7mh3ikbsscvta83ecgev03k',
            '_ga_L0N0B74HJP': 'GS1.1.1730309329.1.1.1730309691.60.0.0',
            'nmg_sp': 'Y'
        }

        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://magnit.ru',
            'Referer': 'https://magnit.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'content-type': 'application/json',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-app-version': '7.0.0',
            'x-client-name': 'magnit',
            'x-device-id': '4545CF1C-9D97-E5ED-C6C2-CE1D3DBA0DB2',
            'x-device-platform': 'Web',
            'x-device-tag': 'disabled',
            'x-new-magnit': 'true',
            'x-platform-version': 'Windows Chrome 132'
        }

        json_data = {
            'aggs': False,
            'geoBoundingBox': {
                'leftTopLatitude': lat + radius,
                'leftTopLongitude': lon - radius,
                'rightBottomLatitude': lat - radius,
                'rightBottomLongitude': lon + radius,
            },
            'limit': count,
            'storeTypes': [
                1,
                2,
                6,
                5,
            ],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://magnit.ru/webgate/v1/store-search/geo',
                json=json_data,
                cookies=cookies,
                headers=headers
            )
            if response.status_code == 200:
                stores_response: list = response.json().get('stores', [])
                return [MagnitStore(store=store) for store in stores_response]

        return []
