from src.airplane import Airplane
from src.airplane_editor import JsonSaver
from src.api_interaction import GetPlanesInfo
from src.utils import filter_by_country, get_top_airplanes, sort_by_altitude


def read_country() -> str:
    while True:
        country = input("Enter country name: ").strip().capitalize()
        if country:
            return country
        print("Country name cannot be empty.")


def read_sorting_num() -> int:
    while True:
        try:
            sorting_num = int(input("Enter number for sorting: ").strip())
            if sorting_num > 0:
                return sorting_num
        except ValueError:
            pass
        print("Enter a positive integer.")


def read_filter_countries() -> list[str]:
    countries = input("Enter countries for filtering: ").split()
    return [country.capitalize() for country in countries]


def user_interaction():
    api = GetPlanesInfo()
    saver = JsonSaver()

    country = read_country()
    sorting_num = read_sorting_num()
    filter_countries = read_filter_countries()

    airplanes_data = api.get_planes(country)
    airplanes = Airplane.to_list(airplanes_data)

    for airplane in airplanes:
        saver.add(airplane)

    if filter_countries:
        airplanes = filter_by_country(airplanes, filter_countries)

        airplanes = sort_by_altitude(airplanes)
        top_airplanes = get_top_airplanes(airplanes, sorting_num)

        for airplane in top_airplanes:
            print(airplane)
