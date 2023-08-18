import requests

api_url = "https://web-gateway.uat.ya.magnit.ru/"
base_url = {
    "getGeolocationCoords": f"{api_url}v1/geolocation/store"
}


def geolocation_coords(e, i):
    i = f"?Latitude={e}&Longitude={i}&Radius=50&Limit=10"
    headers = {
        "x-platform-version": "window.navigator.userAgent",
        "x-device-id": "x5glri6mny",
        "x-device-tag": "disabled",
        "x-app-version": "0.1.0",
        "x-device-platform": "Web",
        "x-client-name": "magnit"
    }

    response = requests.get(base_url["getGeolocationCoords"] + i, headers=headers)
    response.raise_for_status()

    return response.json()


result = geolocation_coords(51.838167, 55.156713)
print(result)





