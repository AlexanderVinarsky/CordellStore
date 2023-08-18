class Goods:
    def __init__(self, goods):
        self.code = goods.code
        self.id = goods.id
        self.name = goods.name
        self.price = goods.offers[0].price
