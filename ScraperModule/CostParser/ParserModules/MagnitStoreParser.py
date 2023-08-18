import json
from types import SimpleNamespace

import requests

from ScraperModule.CostParser.Objects.MagnitStore import MagnitStore

api_url = "https://web-gateway.uat.ya.magnit.ru/"
base_url = {
    "getGeolocationCoords": f"{api_url}v1/geolocation/store"
}


def get_near_magnit_stores(x, y, radius, count):
    i = f"?Latitude={x}&Longitude={y}&Radius={radius}&Limit={count}"
    headers = {
        "x-platform-version": "window.navigator.userAgent",
        "x-device-id": "x5glri6mny",
        "x-device-tag": "disabled",
        "x-app-version": "0.1.0",
        "x-device-platform": "Web",
        "x-client-name": "magnit"
    }

    response = json.loads(requests.get(base_url["getGeolocationCoords"] + i,
                                       headers=headers).text, object_hook=lambda d: SimpleNamespace(**d))

    stores = []
    for store in response.stores:
        stores.append(MagnitStore(store=store))

    return stores

