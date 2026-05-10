import csv
import json
from abc import ABC, abstractmethod


class BaseEditor(ABC):
    @abstractmethod
    def add(self, airplane):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, airplane):
        pass


class JsonSaver(BaseEditor):
    def __init__(self, filename="data.json"):
        self.filename = filename

    def _read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as json_file:
                return json.load(json_file)

        except Exception as e:
            print("Impossible to open the file", e)
            return []

    def _write(self, data):
        with open(self.filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def add(self, airplane):
        data = self._read()
        data.append(airplane.to_dict())
        self._write(data)

    def get(self, **kwargs):
        data = self._read()
        result = []

        for i in data:
            match = True
            for key, value in kwargs.items():
                if i.get(key) != value:
                    match = False

            if match:
                result.append(i)

        return result

    def delete(self, airplane):
        data = self._read()
        data = [i for i in data if i["callsign"] != airplane.callsign]
        self._write(data)


class CsvSaver(BaseEditor):
    def __init__(self, filename="data.csv"):
        self.filename = filename
        self.fields = [
            "icao24",
            "callsign",
            "origin_country",
            "time_position",
            "last_contact",
            "longitude",
            "latitude",
            "baro_altitude",
            "on_ground",
            "velocity",
            "true_track",
            "vertical_rate",
            "sensors",
            "geo_altitude",
            "squawk",
            "position_source",
        ]

    def _read(self):
        data = []
        try:
            with open(self.filename, "r", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print("Impossible to open the file", e)
            pass
        return data

    def _write(self, data):
        with open(self.filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(data)

    def add(self, airplane):
        data = self._read()
        data.append(airplane.to_dict())
        self._write(data)

    def get(self, **kwargs):
        data = self._read()
        result = []

        for i in data:
            match = True
            for key, value in kwargs.items():
                if i.get(key) != value:
                    match = False

            if match:
                result.append(i)

        return result

    def delete(self, airplane):
        data = self._read()
        data = [i for i in data if i["callsign"] != airplane.callsign]
        self._write(data)


class TxtSaver(BaseEditor):
    def __init__(self, filename="data.txt"):
        self.filename = filename

    def _read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as txt_file:
                return txt_file.readlines()
        except Exception as e:
            print("Impossible to open the file", e)
            return []

    def _write(self, lines):
        with open(self.filename, "w", encoding="utf-8") as txt_file:
            txt_file.writelines(lines)

    def add(self, airplane):
        with open(self.filename, "a", encoding="utf-8") as txt_file:
            txt_file.write(str(airplane) + "\n")

    def get(self, **kwargs):
        lines = self._read()
        result = []

        for i in lines:
            match = True
            for key, value in kwargs.items():
                if value not in i:
                    match = False
                    break

            if match:
                result.append(i.strip())

        return result

    def delete(self, airplane):
        lines = self._read()
        lines = [i for i in lines if airplane.callsign not in i]
        self._write(lines)
