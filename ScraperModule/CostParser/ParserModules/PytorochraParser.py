import json
import math
from types import SimpleNamespace

import requests

stores_url = "https://5ka.ru/api/v3/stores/in-area"
products_url = "https://5ka.ru/api/v2/special_offers/"


def pase_stores(x, y, radius):
    min_lat, max_lat, min_lon, max_lon = generate_bbox(x, y, radius)
    stores_headers = {
        "bbox": f"{min_lat},{min_lon},{max_lat},{max_lon}"
    }

    return json.loads(requests.get(stores_url, params=stores_headers).text, object_hook=lambda d: SimpleNamespace(**d))


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
        "X-User-Store": f"{store.sap_code}",
        "X-Authorization": "Bearer "

    }

    products_params = {
        f"limit": f"{products_count}",
    }

    return json.loads(requests.get(products_url, headers=products_header, params=products_params).text,
                      object_hook=lambda d: SimpleNamespace(**d))