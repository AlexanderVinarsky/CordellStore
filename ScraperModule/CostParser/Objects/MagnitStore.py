from ScraperModule.CostParser.Objects.Store import Store


class MagnitStore(Store):
    def __init__(self, store):
        self.name = "Магнит"
        self.company_name = "Магнит"
        super().__init__(None)

        if store is not None:
            self.code = store.code
            self.x_coordinate = store.latitude
            self.y_coordinate = store.longitude

            self.open_hours = [store.openingHours, store.closingHours]
        else:
            self.code = 0
            self.x_coordinate = 0
            self.y_coordinate = 0

            self.open_hours = ["0", "0"]
