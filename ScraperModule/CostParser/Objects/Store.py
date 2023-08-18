class Store:
    def __init__(self, feature):
        if feature is not None:
            self.name = feature.properties.name
            self.company_name = feature.properties.CompanyMetaData.name

            self.x_coordinate = feature.geometry.coordinates[0]
            self.y_coordinate = feature.geometry.coordinates[1]

            self.open_hours = feature.properties.CompanyMetaData.Hours.Availabilities
