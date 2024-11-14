import os

from fastapi_redis_cache import FastApiRedisCache, cache
from fastapi import FastAPI, status, Request, Response, HTTPException

from scrapper.objects.store import Store
from scrapper.objects.magnit.magnit import MagnitStore
from scrapper.objects.common import get_coordinates_by_address


app = FastAPI()
LOCAL_REDIS_URL = "redis://127.0.0.1:6379"


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="api-cache",
        response_header="X-API-Cache",
        ignore_arg_types=[Request, Response]
    )
    

@app.get("/geo:get_coordinates:near_shops")
async def _get_shop_coordinates(address: str, limit: int = 1) -> dict:
    return {
        "data": [x.to_json() for x in Store.parse_near_stores(address)[:limit]]
    }


@app.get("/geo:get_coordinates:by_querry")
async def _get_coordinates(address: str) -> dict:
    coordinates = get_coordinates_by_address(address)
    if coordinates is None:
        raise HTTPException(status_code=404, detail="Coordinates not found")
    
    lat, lon = coordinates
    return {
        "data": [ round(float(lat), 2), round(float(lon), 2) ]
    }


@app.get("/shop:get_products")
async def _get_products(lat: float, lon: float, shop_type: str = "magnit") -> dict:
    if shop_type == "magnit":
        try:
            store: Store = MagnitStore.get_near_magnit_stores(lat, lon, .02)[-1]
        except Exception as ex:
            raise HTTPException(status_code=500, detail="Index error") from ex

    if len(store.storage) == 0:
        raise HTTPException(status_code=400, detail="No products in store!")

    return {
        "data": [ x.to_json() for x in store.storage ]
    }


@app.get("/heatmap:get")
async def _get_heatmap(
    upper_bound: tuple[float, float],
    lower_bound: tuple[float, float],
    product: str,
    shop_type: str = "magnit"
) -> dict:
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

    if len(product_data) == 0:
        raise HTTPException(status_code=404, detail="Product not found!")
    
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
        "data": [{"lat": p["lat"], "lon": p["lon"], "intensity": p["normalized_price"] * 100} for p in product_data]
    }
