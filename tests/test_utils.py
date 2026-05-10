import pytest

from src.airplane import Airplane
from src.utils import filter_by_country, get_top_airplanes, sort_by_altitude


def make_airplane(callsign: str, country: str, altitude: float) -> Airplane:
    return Airplane(
        icao24=callsign.lower(),
        callsign=callsign,
        origin_country=country,
        time_position=1,
        last_contact=2,
        longitude=1.0,
        latitude=1.0,
        baro_altitude=altitude - 100,
        on_ground=False,
        velocity=200.0,
        true_track=90.0,
        vertical_rate=0.0,
        sensors=[],
        geo_altitude=altitude,
        squawk="7000",
        position_source=0,
    )


@pytest.fixture
def airplanes():
    return [
        make_airplane("RO1", "Romania", 1000),
        make_airplane("DE1", "Germany", 3000),
        make_airplane("FR1", "France", 2000),
    ]


def test_filter_by_country_returns_only_matching_airplanes(airplanes):
    result = filter_by_country(airplanes, ["Romania", "Germany"])

    assert [plane.callsign for plane in result] == ["RO1", "DE1"]


def test_sort_by_altitude_descending(airplanes):
    result = sort_by_altitude(airplanes)

    assert [plane.callsign for plane in result] == ["DE1", "FR1", "RO1"]


def test_get_top_airplanes_limits_result_count(airplanes):
    result = get_top_airplanes(airplanes, 2)

    assert [plane.callsign for plane in result] == ["RO1", "DE1"]
