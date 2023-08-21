from ScraperModule.CostParser.Objects.Store import Store


class PyatorochkaStore(Store):
    def __init__(self, store):
        self.name = "Пятёрочка"
        self.company_name = "Пятёрочка"
        super().__init__(None)

        if store is not None:
            self.code = store.sap_code
            self.x_coordinate = store.lat
            self.y_coordinate = store.lon

            self.open_hours = [store.work_start_time, store.work_end_time]
        else:
            self.code = 0
            self.x_coordinate = 0
            self.y_coordinate = 0

            self.open_hours = ["0", "0"]
