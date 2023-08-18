import requests
import json
from types import SimpleNamespace

from ScraperModule.CostParser.Objects.Store import Store


def parse_near_stores(place, count):
    location_request = "https://search-maps.yandex.ru/v1/?apikey=a0a1e035-9501-415c-a135-2375d508d6a3" \
                      f"&text={place}&lang=ru_RU&type=biz&results={count}"

    response = json.loads(requests.get(location_request).text, object_hook=lambda d: SimpleNamespace(**d))

    stores = []
    for store in response.features:
        stores.append(Store(feature=store))

    return stores
