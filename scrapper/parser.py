import sys

sys.path.append('C:/Users/j1sk1ss/RiderProjects/Cordell.Stores')
from scrapper.objects.product import Product
from scrapper.objects.store import Store
from scrapper.objects.magnit.magnit import MagnitStore


# Get average prices from all goods
def stores_average_price(stores: list[Store]) -> list[Product]:
    average_goods: list[Product] = []
    for store in stores:
        for good in store.storage:
            for i in range(len(average_goods)):
                if average_goods[i].name == good.name:
                    average_goods[i].price = (float(str(average_goods[i].price).replace(",", ".")) + float(str(good.price).replace(",", "."))) / 2

            average_goods.append(good)

    return average_goods


def stores_price_scattering(stores: list[list[Store]]) -> tuple:
    names: list = []
    max_price: list = []
    min_price: list = []

    for store in stores:
        for products in stores_average_price(store):
            price: float = float(str(products.price).replace(",", "."))
            for i in range(len(names)):
                # Checking name of product (put here NLP model)
                if names[i] == products.name:
                    if max_price[i] <= price:
                        max_price[i] = price
                    if min_price[i] >= price:
                        min_price[i] = price
                    break
            else:
                names.append(products.name)
                min_price.append(price)
                max_price.append(price)

    return names, min_price, max_price


stores: list = []
for place in ["Россия, Оренбург, Магнит", "Россия, Москва, Магнит"]:
    stores.append(MagnitStore.load_magnit_stores(place=place, store_count=50))

names, min_price, max_price = stores_price_scattering(stores)
for i in range(len(names)):
    print(str(names[i]) + ": " + str(min_price[i]) + " -> " + str(max_price[i]))