from ScraperModule.CostParser.Objects.Store import Store


class MagnitStore(Store):
    storage = []

    def __init__(self, store):
        super().__init__(None)
        self.name = "Магнит"
        self.company_name = "Магнит"

        self.code = store.code
        self.x_coordinate = store.latitude
        self.y_coordinate = store.longitude

        self.open_hours = [store.openingHours, store.closingHours]
