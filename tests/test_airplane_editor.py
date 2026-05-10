import pytest

from src.airplane import Airplane
from src.airplane_editor import CsvSaver, JsonSaver, TxtSaver


@pytest.fixture
def airplane():
    return Airplane(
        icao24="ro123",
        callsign="RO123",
        origin_country="Romania",
        time_position=1,
        last_contact=2,
        longitude=1.0,
        latitude=1.0,
        baro_altitude=900.0,
        on_ground=False,
        velocity=200.0,
        true_track=90.0,
        vertical_rate=0.0,
        sensors=[],
        geo_altitude=1000.0,
        squawk="7000",
        position_source=0,
    )


def test_json_saver_add_get_delete(tmp_path, airplane):
    filename = tmp_path / "airplanes.json"
    saver = JsonSaver(str(filename))

    saver.add(airplane)
    stored = saver.get(callsign="RO123")

    assert len(stored) == 1
    assert stored[0]["origin_country"] == "Romania"

    saver.delete(airplane)
    assert saver.get(callsign="RO123") == []


def test_csv_saver_add_get_delete(tmp_path, airplane):
    filename = tmp_path / "airplanes.csv"
    saver = CsvSaver(str(filename))

    saver.add(airplane)
    stored = saver.get(callsign="RO123")

    assert len(stored) == 1
    assert stored[0]["callsign"] == "RO123"

    saver.delete(airplane)
    assert saver.get(callsign="RO123") == []


def test_txt_saver_add_get_delete(tmp_path, airplane):
    filename = tmp_path / "airplanes.txt"
    saver = TxtSaver(str(filename))

    saver.add(airplane)
    stored = saver.get(callsign="RO123")

    assert len(stored) == 1
    assert "RO123" in stored[0]

    saver.delete(airplane)
    assert saver.get(callsign="RO123") == []
