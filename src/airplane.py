class Airplane:
    def __init__(
        self,
        icao24: str,
        callsign: str | None,
        origin_country: str,
        time_position: int | None,
        last_contact: int,
        longitude: float | None,
        latitude: float | None,
        baro_altitude: float | None,
        on_ground: bool,
        velocity: float | None,
        true_track: float | None,
        vertical_rate: float | None,
        sensors: list[int] | None,
        geo_altitude: float | None,
        squawk: str | None,
        position_source: int,
    ):
        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else "Unknown"
        self.origin_country = origin_country

        self.time_position = time_position if self.valid_number(time_position) else None
        self.last_contact = last_contact

        self.longitude = self.valid_float(longitude)
        self.latitude = self.valid_float(latitude)

        self.baro_altitude = self.valid_float(baro_altitude)
        self.geo_altitude = self.valid_float(geo_altitude)
        self.velocity = self.valid_float(velocity)
        self.true_track = self.valid_float(true_track)
        self.vertical_rate = float(vertical_rate) if vertical_rate is not None else 0.0

        self.on_ground = bool(on_ground)
        self.sensors = sensors if sensors else []
        self.squawk = squawk if squawk else "Unknown"
        self.position_source = position_source

    def valid_number(self, value):
        return value is not None and value >= 0

    def valid_float(self, value):
        return float(value) if value is not None else 0.0

    def __lt__(self, other):
        return self.geo_altitude < other.geo_altitude

    def __gt__(self, other):
        return self.geo_altitude > other.geo_altitude

    def __str__(self):
        return (
            f"{self.callsign} ({self.icao24}) from {self.origin_country}: "
            f"altitude={self.geo_altitude}, velocity={self.velocity}"
        )

    def compare_speed(self, other):
        return self.velocity - other.velocity

    def to_dict(self):
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "time_position": self.time_position,
            "last_contact": self.last_contact,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "baro_altitude": self.baro_altitude,
            "on_ground": self.on_ground,
            "velocity": self.velocity,
            "true_track": self.true_track,
            "vertical_rate": self.vertical_rate,
            "sensors": self.sensors,
            "geo_altitude": self.geo_altitude,
            "squawk": self.squawk,
            "position_source": self.position_source,
        }

    @staticmethod
    def to_list(data: list):
        result = []
        for item in data:
            if not isinstance(item, list) or len(item) < 17:
                print(f"Skipping malformed airplane record: {item}")
                continue

            try:
                plane = Airplane(
                    icao24=item[0],
                    callsign=item[1],
                    origin_country=item[2],
                    time_position=item[3],
                    last_contact=item[4],
                    longitude=item[5],
                    latitude=item[6],
                    baro_altitude=item[13],
                    on_ground=item[8],
                    velocity=item[9],
                    true_track=item[10],
                    vertical_rate=item[11],
                    sensors=item[12],
                    geo_altitude=item[7],
                    squawk=item[14],
                    position_source=item[16],
                )
                result.append(plane)
            except (TypeError, ValueError, IndexError) as error:
                print(f"Impossible to make a list item: {error}")
        return result
