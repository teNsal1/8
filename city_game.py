import json
from dataclasses import dataclass
from typing import List, Dict, Set, Optional

# Датаклассы и вспомогательные классы
@dataclass
class City:
    # Датакласс для представления города
    name: str
    population: int
    subject: str
    district: str
    latitude: str
    longitude: str
    is_used: bool = False

class JsonFile:
    # Работы с JSON-файлами
    def __init__(self, filepath: str):
        self.filepath = filepath

    def read_data(self) -> List[Dict]:
        # Чтение данных из JSON-файла
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.filepath} не найден!")
            return []

    def write_data(self, data: List[Dict]) -> None:
        # Запись данных в JSON-файл
        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

class CitiesSerializer:
    # Класс для сериализации данных о городах
    def __init__(self, city_data: List[Dict]):
        self.cities = [
            City(
                name=city['name'],
                population=city['population'],
                subject=city['subject'],
                district=city['district'],
                latitude=city['coords']['lat'],
                longitude=city['coords']['lon']
            ) for city in city_data
        ]

    def get_all_cities(self) -> List[City]:
        # Получить все города
        return self.cities
    
