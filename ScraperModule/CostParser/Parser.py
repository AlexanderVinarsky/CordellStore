from ScraperModule.CostParser import MagnitCostParser, MagnitStoreParser, StorePlaceParser


def Parse(place, count=50):
    goods = []

    for store in StorePlaceParser.parse_near_stores(place, count):
        for good in MagnitCostParser.parse_products(
                MagnitStoreParser.get_near_magnit_stores(store.x_coordinate, store.y_coordinate, 50, 1)[0]):
            goods.append(good)

    return goods


print(Parse("Оренбург Прострорная Магнит", 1)[0].price)