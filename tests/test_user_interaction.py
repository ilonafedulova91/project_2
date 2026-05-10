from unittest.mock import patch

import pytest

from src.airplane import Airplane
from src.user_interaction import (read_country, read_filter_countries,
                                  read_sorting_num, user_interaction)


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
def sample_airplanes():
    return [
        make_airplane("RO_LOW", "Romania", 1000),
        make_airplane("DE_HIGH", "Germany", 3000),
        make_airplane("RO_HIGH", "Romania", 2500),
    ]


def test_read_country_retries_until_non_empty():
    with patch("builtins.input", side_effect=["", "romania"]):
        assert read_country() == "Romania"


def test_read_sorting_num_retries_until_positive_integer():
    with patch("builtins.input", side_effect=["abc", "0", "3"]):
        assert read_sorting_num() == 3


def test_read_filter_countries_capitalizes_words():
    with patch("builtins.input", return_value="romania germany"):
        assert read_filter_countries() == ["Romania", "Germany"]


def test_user_interaction_saves_filters_sorts_and_prints(sample_airplanes, capsys):
    fake_raw_data = [["raw-state"]]

    with patch("builtins.input", side_effect=["Romania", "2", "Romania Germany"]):
        with patch("src.user_interaction.GetPlanesInfo") as mock_api_cls:
            with patch("src.user_interaction.JsonSaver") as mock_saver_cls:
                with patch(
                    "src.user_interaction.Airplane.to_list",
                    return_value=sample_airplanes,
                ):
                    mock_api = mock_api_cls.return_value
                    mock_api.get_planes.return_value = fake_raw_data

                    mock_saver = mock_saver_cls.return_value

                    user_interaction()

    captured = capsys.readouterr()

    mock_api.get_planes.assert_called_once_with("Romania")
    assert mock_saver.add.call_count == 3
    assert "DE_HIGH" in captured.out
    assert "RO_HIGH" in captured.out
