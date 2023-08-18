from ScraperModule.CostParser import MagnitCostParser, MagnitStoreParser, StorePlaceParser


def Parse(place, goods_count=36, store_count=50):
    stores = []

    # Get stores by yandex API
    for store in StorePlaceParser.parse_near_stores(place, store_count):
        store_goods = []
        for current_good in MagnitCostParser.parse_products(
                # Get magnit stores near cords, that was taken from yandex API
                MagnitStoreParser.get_near_magnit_stores(store.x_coordinate, store.y_coordinate, 50, 1)[0], goods_count):
            store_goods.append(current_good)

        store.storage = store_goods
        stores.append(store)

    return stores


def AveragePrices(stores):
    average_goods = []
    for store in stores:
        for good in store.storage:
            for i in range(len(average_goods)):
                if average_goods[i].name == good.name:
                    average_price = str(average_goods[i].price).replace(",", ".")
                    current_price = str(good.price).replace(",", ".")

                    average_goods[i].price = (float(average_price) + float(current_price)) / 2

            average_goods.append(good)

    return average_goods


# Example of using
for product in AveragePrices(Parse("Оренбург Прострорная Магнит", 200, 50)):
    print(str(product.name) + " " + str(product.price))