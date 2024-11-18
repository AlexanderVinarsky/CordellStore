import redis
import pickle

from rapidfuzz import fuzz

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from scrapper.objects.store import Store
from scrapper.objects.magnit.magnit import MagnitStore
from scrapper.objects.common import get_coordinates_by_address


app = FastAPI()
rd = redis.Redis(host="app-redis-1", port=6379, db=0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/geo/get_coordinates/near_shops")
async def _get_shop_coordinates(address: str, limit: int = 1) -> dict:
    cached_data = rd.get(f"0{address}{limit}")
    if cached_data:
        return pickle.loads(cached_data)
    
    try:
        data: dict = {
            "data": [x.to_json() for x in Store.parse_near_stores(address)[:limit]]
        }
    except Exception as ex:
        raise HTTPException(status_code=500, detail="_get_shop_coordinates: Parsing error") from ex

    rd.set(f"{address}{limit}", pickle.dumps(data))
    return data


@app.get("/geo/get_coordinates/by_querry")
async def _get_coordinates(address: str) -> dict:
    cached_data = rd.get(f"1{address}")
    if cached_data:
        return pickle.loads(cached_data)
    
    coordinates = get_coordinates_by_address(address)
    if coordinates is None:
        raise HTTPException(status_code=404, detail="_get_coordinates: Coordinates not found")
    
    lat, lon = coordinates
    data = {
        "data": [ round(float(lat), 2), round(float(lon), 2) ]
    }
    
    rd.set(f"1{address}", pickle.dumps(data))
    return data


@app.get("/shop/get_products")
async def _get_products(lat: float, lon: float, shop_type: str = "magnit") -> dict:
    cached_data = rd.get(f"2{lat}{lon}{shop_type}")
    if cached_data:
        return pickle.loads(cached_data)
    
    if shop_type == "magnit":
        try:
            stores: list[Store] = await MagnitStore.get_near_magnit_stores(lat, lon, .02)
            store: Store = stores[-1]
        except Exception as ex:
            raise HTTPException(status_code=500, detail="get_near_magnit_stores: Index error") from ex

    if len(store.storage) == 0:
        raise HTTPException(status_code=400, detail="_get_products: No products in store!")

    data = {
        "data": [ x.to_json() for x in store.storage ]
    }
    
    rd.set(f"2{lat}{lon}{shop_type}", pickle.dumps(data))
    return data


@app.get("/heatmap/get")
async def _get_heatmap(
    center_lat: float,
    center_lon: float,
    radius: float,
    product: str,
    shop_type: str = "magnit",
    shops_limit: int = 5
) -> dict:
    cached_data = rd.get(f"3{center_lat}{center_lon}{radius}{product}{shop_type}{shops_limit}")
    if cached_data:
        return pickle.loads(cached_data)
    
    if shop_type == "magnit":
        stores: list[Store] = await MagnitStore.get_near_magnit_stores(center_lat, center_lon, radius, shops_limit)
    elif shop_type == "lenta":
        pass
    else:
        raise HTTPException(status_code=404, detail="_get_heatmap: Shop type not supported")

    product_data = []
    for store in stores:
        for item in store.storage:
            if fuzz.partial_ratio(item.name.lower(), product.lower()) > 75:
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

    data = {
        "data": [{"lat": p["lat"], "lng": p["lon"], "intensity": p["normalized_price"] * 100} for p in product_data]
    }
    
    rd.set(f"3{center_lat}{center_lon}{radius}{product}{shop_type}{shops_limit}", pickle.dumps(data))
    return data
