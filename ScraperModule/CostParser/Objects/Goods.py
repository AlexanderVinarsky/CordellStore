class Goods:
    def __init__(self, goods):
        if goods is not None:
            self.code = goods.code
            self.id = goods.id
            self.name = goods.name

            if len(goods.offers) > 0:
                self.price = goods.offers[0].price
            else:
                self.price = 0
        else:
            self.code = 0
            self.id = 0
            self.name = ''
            self.price = 0
