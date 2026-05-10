def filter_by_country(data, countries):
    return [airplane for airplane in data if airplane.origin_country in countries]


def sort_by_altitude(data):
    return sorted(data, key=lambda airplane: airplane.geo_altitude, reverse=True)


def get_top_airplanes(data, num):
    return data[:num]
