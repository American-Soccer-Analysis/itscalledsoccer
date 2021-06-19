class Stadium:
    def __init__(
        self,
        stadium_id: str,
        stadium_name: str,
        capacity: int = None,
        year_built: int = None,
        roof: bool = None,
        turf: bool = None,
        street: str = None,
        city: str = None,
        province: str = None,
        country: str = None,
        postal_code: str = None,
        latitude: float = None,
        longitude: float = None,
        field_x: int = None,
        field_y: int = None,
    ) -> None:
        self.stadium_id = stadium_id
        self.stadium_name = stadium_name
        self.capacity = capacity
        self.year_built = year_built
        self.roof = roof
        self.turf = turf
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.field_x = field_x
        self.field_y = field_y


class Stadia:
    pass
