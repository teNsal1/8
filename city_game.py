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
    
class CityGame:
    # Класс для управления логикой игры
    def __init__(self, cities: CitiesSerializer):
        self.all_cities = {city.name.lower(): city for city in cities.get_all_cities()}
        self.used_cities: Set[str] = set()
        self.last_letter: Optional[str] = None
        self.bad_letters: Set[str] = self._calculate_bad_letters()

    def _calculate_bad_letters(self) -> Set[str]:
        # Определить 'плохие' буквы, на которые нет городов
        bad_letters = set()
        for letter in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            if not any(city.lower().startswith(letter) for city in self.all_cities):
                bad_letters.add(letter)
        return bad_letters

    def start_game(self) -> None:
        # Начать игру с хода компьютера
        computer_city = next(iter(self.all_cities.values()))
        print(f"Компьютер начинает: {computer_city.name}")
        self.used_cities.add(computer_city.name.lower())
        self.last_letter = computer_city.name[-1].lower()

    def human_turn(self, city_input: str) -> bool:
        # Обработать ход человека
        city = self.all_cities.get(city_input.lower())
        if not city:
            print("Город не найден!")
            return False
        if self.last_letter and city_input[0].lower() != self.last_letter:
            print(f"Город должен начинаться на букву '{self.last_letter.upper()}'!")
            return False
        self.used_cities.add(city_input.lower())
        self.last_letter = city_input[-1].lower()
        return True

    def computer_turn(self) -> Optional[str]:
        # Ход компьютера
        possible_cities = [
            name for name in self.all_cities
            if name[0] == self.last_letter
            and name not in self.used_cities
            and name[-1] not in self.bad_letters
        ]
        if not possible_cities:
            return None
        chosen_city = possible_cities[0]
        self.used_cities.add(chosen_city)
        self.last_letter = chosen_city[-1]
        return chosen_city.capitalize()
    
class GameManager:
    # Фасад для управления игрой
    def __init__(self, json_file: JsonFile, cities_serializer: CitiesSerializer, city_game: CityGame):
        self.json_file = json_file
        self.cities_serializer = cities_serializer
        self.city_game = city_game

    def __call__(self) -> None:
        # Запуск игры
        self.city_game.start_game()
        while True:
            # Ход человека
            human_input = input("Ваш ход: ").strip()
            if not self.city_game.human_turn(human_input):
                print("Вы проиграли!")
                break
            
            # Ход компьютера
            computer_city = self.city_game.computer_turn()
            if not computer_city:
                print("Компьютер проиграл!")
                break
            print(f"Компьютер: {computer_city}")

if __name__ == "__main__":
    # Инициализация компонентов
    json_file = JsonFile("cities.json")
    cities_serializer = CitiesSerializer(json_file.read_data())
    city_game = CityGame(cities_serializer)
    
    # Запуск игры через фасад
    game_manager = GameManager(json_file, cities_serializer, city_game)
    game_manager()