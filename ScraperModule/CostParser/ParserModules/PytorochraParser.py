import json
import math
from types import SimpleNamespace

import requests

from ScraperModule.CostParser.Objects.Goods import Goods
from ScraperModule.CostParser.Objects.PyatorochkaStore import PyatorochkaStore

stores_url = "https://5d.5ka.ru/api/v3/stores/in-area"
products_url = "https://5ka.ru/api/v2/special_offers/"


def pase_stores(x, y, radius):
    min_lat, max_lat, min_lon, max_lon = generate_bbox(x, y, radius)
    stores_headers = {
        "bbox": f"{min_lat},{min_lon},{max_lat},{max_lon}"
    }

    try:
        stores = []
        for store in json.loads(requests.get(stores_url, params=stores_headers).text, object_hook=lambda d: SimpleNamespace(**d)):
            stores.append(PyatorochkaStore(store=store))

        return stores
    except Exception as e:
        return [PyatorochkaStore(None)]


def generate_bbox(latitude, longitude, distance_meters):
    earth_radius = 6371000
    lat_distance_deg = distance_meters / earth_radius * (180 / math.pi)

    lon_distance_deg = distance_meters / (earth_radius * math.cos(math.radians(latitude))) * (180 / math.pi)

    min_lat = latitude - lat_distance_deg
    max_lat = latitude + lat_distance_deg
    min_lon = longitude - lon_distance_deg
    max_lon = longitude + lon_distance_deg

    return min_lat, max_lat, min_lon, max_lon


def parse_products(store, products_count):
    products_header = {
        "X-User-Store": f"{store.code}",
        "X-Authorization": "Bearer "

    }

    products_params = {
        f"limit": f"{products_count}",
    }

    try:
        goods_list = []
        for goods in json.loads(requests.get(products_url, headers=products_header, params=products_params).text,
                                object_hook=lambda d: SimpleNamespace(**d)).results:
            product = Goods(None)

            product.code = goods.plu
            product.name = goods.name
            product.price = goods.current_prices.price_reg__min
            product.id = goods.id

            goods_list.append(product)

        return goods_list
    except Exception as e:
        return [Goods(None)]

