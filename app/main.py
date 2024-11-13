import os

from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
from fastapi_redis_cache import FastApiRedisCache


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