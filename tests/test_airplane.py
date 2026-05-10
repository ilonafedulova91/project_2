import pytest

from src.airplane import Airplane


@pytest.fixture
def sample_state():
    return [
        "abc123",  # icao24
        "TEST123 ",  # callsign
        "Romania",  # origin_country
        100,  # time_position
        200,  # last_contact
        26.1,  # longitude
        44.4,  # latitude
        1100.0,  # geo_altitude in current parser
        False,  # on_ground
        250.0,  # velocity
        180.0,  # true_track
        5.5,  # vertical_rate
        [1, 2],  # sensors
        1000.0,  # baro_altitude in current parser
        "7000",  # squawk
        False,  # spi
        0,  # position_source
    ]


@pytest.fixture
def airplane():
    return Airplane(
        icao24="abc123",
        callsign="TEST123",
        origin_country="Romania",
        time_position=100,
        last_contact=200,
        longitude=26.1,
        latitude=44.4,
        baro_altitude=1000.0,
        on_ground=False,
        velocity=250.0,
        true_track=180.0,
        vertical_rate=5.5,
        sensors=[1, 2],
        geo_altitude=1100.0,
        squawk="7000",
        position_source=0,
    )


def test_airplane_normalizes_values():
    plane = Airplane(
        icao24="abc123",
        callsign=None,
        origin_country="Romania",
        time_position=None,
        last_contact=200,
        longitude=None,
        latitude=44.4,
        baro_altitude=None,
        on_ground=False,
        velocity=None,
        true_track=None,
        vertical_rate=None,
        sensors=None,
        geo_altitude=None,
        squawk=None,
        position_source=0,
    )

    assert plane.callsign == "Unknown"
    assert plane.time_position is None
    assert plane.longitude == 0.0
    assert plane.baro_altitude == 0.0
    assert plane.velocity == 0.0
    assert plane.vertical_rate == 0.0
    assert plane.sensors == []
    assert plane.squawk == "Unknown"


def test_airplane_to_dict_contains_expected_fields(airplane):
    data = airplane.to_dict()

    assert data["icao24"] == "abc123"
    assert data["callsign"] == "TEST123"
    assert data["origin_country"] == "Romania"
    assert data["geo_altitude"] == 1100.0
    assert data["position_source"] == 0


def test_to_list_converts_valid_state_rows(sample_state):
    airplanes = Airplane.to_list([sample_state])

    assert len(airplanes) == 1
    plane = airplanes[0]
    assert plane.icao24 == "abc123"
    assert plane.callsign == "TEST123"
    assert plane.origin_country == "Romania"
    assert plane.geo_altitude == 1100.0
    assert plane.baro_altitude == 1000.0


def test_to_list_skips_malformed_rows(capsys):
    malformed = ["too", "short"]
    airplanes = Airplane.to_list([malformed])

    captured = capsys.readouterr()
    assert airplanes == []
    assert "Skipping malformed airplane record" in captured.out


def test_compare_speed_and_ordering():
    slower = Airplane(
        "one",
        "ONE",
        "Romania",
        1,
        2,
        1.0,
        1.0,
        100.0,
        False,
        150.0,
        0.0,
        0.0,
        [],
        100.0,
        "7000",
        0,
    )
    faster = Airplane(
        "two",
        "TWO",
        "Romania",
        1,
        2,
        1.0,
        1.0,
        200.0,
        False,
        250.0,
        0.0,
        0.0,
        [],
        200.0,
        "7000",
        0,
    )

    assert slower < faster
    assert faster > slower
    assert faster.compare_speed(slower) == 100.0
