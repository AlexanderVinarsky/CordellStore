from __future__ import annotations

from OSMPythonTools.nominatim import Nominatim
from scrapper.objects.product import Product


class Store:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.x_coordinate: float = float(lat)
        self.y_coordinate: float = float(lon)
        self.storage: set[Product] = set()

    @staticmethod
    def parse_near_stores(place: str) -> list[Store]:
        nominatim = Nominatim()
        result = nominatim.query(place)
        stores = []    
        
        if result is not None:
            for store_data in vars(result)['_json']:
                stores.append(Store(lat=store_data['lat'], lon=store_data['lon'], name='none'))
        else:
            return None

        return stores