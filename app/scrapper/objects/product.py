class Product:
    def __init__(self, goods: dict):
        self.code = goods.get('productId', 0)
        self.id = goods.get('id', 0)
        self.name = goods.get('name', 'none')
        self.price = goods.get('price', 0) * .001

    def to_json(self) -> dict:
        return {
            'code': self.code,
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
