from abc import ABC, abstractmethod

from requests import get


class ApiInteraction(ABC):
    @abstractmethod
    def get_coordinates(self, country: str):
        pass

    @abstractmethod
    def get_planes(self, country: str):
        pass


class GetPlanesInfo(ApiInteraction):
    def __init__(self) -> None:
        self.coordinates_url = "https://nominatim.openstreetmap.org/search"
        self.planes_url = "https://opensky-network.org/api/states/all"

    def get_coordinates(self, country: str):
        headers = {"User-Agent": "test-app"}
        params = {
            "q": country,
            "format": "json",
            "limit": 1,
        }

        try:
            response = get(
                url=self.coordinates_url, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            payload = response.json()
            if not payload:
                return None
            return payload[0].get("boundingbox")
        except Exception as error:
            print(
                f"An error occurred while getting a response from openstreetmap.org: {error}"
            )
            return None

    def get_planes(self, country: str):
        coordinates = self.get_coordinates(country)

        if not coordinates or len(coordinates) < 4:
            print("No coordinates found for the selected country.")
            return []

        params = {
            "lamin": coordinates[0],
            "lamax": coordinates[1],
            "lomin": coordinates[2],
            "lomax": coordinates[3],
        }

        try:
            response = get(url=self.planes_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("states", [])
        except Exception as e:
            print(
                f"An error occurred while getting a response from opensky-network.org: {e}"
            )
            return []
