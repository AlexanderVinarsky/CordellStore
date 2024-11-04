from api import app
from fastapi_redis_cache import cache

from scrapper.objects.store import Store
from scrapper.objects.magnit.magnit import MagnitStore
from scrapper.objects.common import get_coordinates_by_address


@app.get("/geo:get_coordinates:near_shops")
@cache(expire=86400)
async def _get_shop_coordinates(address: str, limit: int = 1) -> list:
    stores: list[dict] = [x.to_json() for x in Store.parse_near_stores(address)[:limit]]
    return stores


@app.get("/geo:get_coordinates:by_querry")
@cache(expire=86400)
async def _get_coordinates(address: str) -> list:
    lat, lon = get_coordinates_by_address(address)
    return {
        'data': [ lat, lon ]
    }


@app.get("/shop:get_products")
@cache(expire=86400)
async def _get_products(lat: float, lon: float, shop_type: str = "magnit") -> list:
    if shop_type == "magnit":
        store: Store = MagnitStore.get_near_magnit_stores(lat, lon, .02)[-1]

    if len(store) != 0:
        return [ x.to_json() for x in store.storage ]
    else:
        return []


@app.get("/heatmap:get")
@cache(expire=86400)
async def _get_heatmap(
    upper_bound: tuple[float, float],
    lower_bound: tuple[float, float],
    product: str,
    shop_type: str = "magnit"
) -> list:
    center_lat = (upper_bound[0] + lower_bound[0]) / 2
    center_lon = (upper_bound[1] + lower_bound[1]) / 2
    
    radius = max(
        abs(upper_bound[0] - center_lat),
        abs(upper_bound[1] - center_lon)
    )
    
    if shop_type == "magnit":
        stores: list[Store] = MagnitStore.get_near_magnit_stores(center_lat, center_lon, radius)

    product_data = []
    for store in stores:
        for item in store.storage:
            if item.name == product:
                product_data.append({
                    "lat": store.x_coordinate,
                    "lon": store.y_coordinate,
                    "price": item.price
                })

    if not product_data:
        return []
    
    prices = [p["price"] for p in product_data]
    min_price = min(prices)
    max_price = max(prices)

    if min_price == max_price:
        for p in product_data:
            p["normalized_price"] = 1.0 
    else:
        for p in product_data:
            p["normalized_price"] = max((p["price"] - min_price) / (max_price - min_price), 1)

    return {
        'data': [{"lat": p["lat"], "lon": p["lon"], "intensity": p["normalized_price"] * 100} for p in product_data]
    }
