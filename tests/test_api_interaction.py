from unittest.mock import patch

import pytest

from src.api_interaction import GetPlanesInfo


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


@pytest.fixture
def api():
    return GetPlanesInfo()


def test_get_coordinates_returns_bounding_box(api):
    with patch(
        "src.api_interaction.get",
        return_value=FakeResponse([{"boundingbox": ["1", "2", "3", "4"]}]),
    ) as mock_get:
        result = api.get_coordinates("Romania")

    assert result == ["1", "2", "3", "4"]
    mock_get.assert_called_once_with(
        url=api.coordinates_url,
        params={"q": "Romania", "format": "json", "limit": 1},
        headers={"User-Agent": "test-app"},
        timeout=10,
    )


def test_get_coordinates_returns_none_for_empty_payload(api):
    with patch(
        "src.api_interaction.get",
        return_value=FakeResponse([]),
    ):
        result = api.get_coordinates("Nowhere")

    assert result is None


def test_get_planes_returns_empty_list_when_coordinates_missing(api, capsys):
    with patch.object(api, "get_coordinates", return_value=None):
        result = api.get_planes("Nowhere")

    captured = capsys.readouterr()
    assert result == []
    assert "No coordinates found" in captured.out


def test_get_planes_uses_bounding_box_and_returns_states(api):
    fake_coordinates = ["1", "2", "3", "4"]
    fake_payload = {"states": [["plane-1"], ["plane-2"]]}

    with patch.object(api, "get_coordinates", return_value=fake_coordinates):
        with patch(
            "src.api_interaction.get",
            return_value=FakeResponse(fake_payload),
        ) as mock_get:
            result = api.get_planes("Romania")

    assert result == [["plane-1"], ["plane-2"]]
    mock_get.assert_called_once_with(
        url=api.planes_url,
        params={
            "lamin": "1",
            "lamax": "2",
            "lomin": "3",
            "lomax": "4",
        },
        timeout=10,
    )
