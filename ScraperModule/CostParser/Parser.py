from ScraperModule.CostParser.ParserModules import MagnitParser, StorePlaceParser, PytorochraParser


# Parse stores with goods near selected place.
# Goods count - count of goods, that will be taken from store.
# Store count - count of stores, that will be parsed near location
def Parse(place, goods_count=36, store_count=50, search_radius=50):
    stores = []

    # Get stores by yandex API
    for store in StorePlaceParser.parse_near_stores(place, store_count):
        store_goods = []

        # Get magnit stores near cords, that was taken from yandex API
        magnits = MagnitParser.get_near_magnit_stores(store.y_coordinate, store.x_coordinate, search_radius, 1)
        if len(magnits) > 0:
            for current_product in MagnitParser.parse_products(magnits[0], goods_count):
                store_goods.append(current_product)

        # Get pyatorochka stores near cords, that was taken from yandex API
        pytorochks = PytorochraParser.pase_stores(store.y_coordinate, store.x_coordinate, search_radius * 10)
        if len(pytorochks) > 0:
            for current_product in PytorochraParser.parse_products(pytorochks[0], goods_count):
                store_goods.append(current_product)

        store.storage = store_goods
        stores.append(store)

    return stores


# Get average prices from all goods
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


# Price scattering between lowest and highest
def PriceScattering(places_stores):
    names = []
    max_price = []
    min_price = []

    for stores in places_stores:
        for products in AveragePrices(stores):
            price = float(str(products.price).replace(",", "."))

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

    return [names, min_price, max_price]


# Example of using
# for product in AveragePrices(Parse("Долгопрудный Продуктовый", goods_count=1, store_count=50)):
    # print(str(product.name) + " " + str(product.price))

# Example of using
# check_places = ["Оренбург Магнит", "Долгопрудный Магнит"]
# answers = []
# for place in check_places:
#     answers.append(Parse(place, goods_count=200, store_count=50))
#
# scattering = PriceScattering(answers)
#
# for i in range(len(scattering[0])):
#     print(str(scattering[0][i]) + ": " + str(scattering[1][i]) + " -> " + str(scattering[2][i]))
