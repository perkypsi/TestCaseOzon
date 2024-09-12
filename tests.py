import pytest
import json
from unittest.mock import mock_open, patch
from app import get_tallest_hero_from_file

# Тест 1: Проверка корректной работы при стандартных данных
def test_tallest_hero_standard_data():
    mock_data = json.dumps([
        {"name": "Hero1", "gender": "male", "height": 180, "work": True},
        {"name": "Hero2", "gender": "male", "height": 190, "work": True},
        {"name": "Hero3", "gender": "female", "height": 170, "work": False},
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_tallest_hero_from_file("male", True, "dummy_path")
    
    assert result["name"] == "Hero2"
    assert result["height"] == 190

# Тест 2: Проверка работы при отсутствии героев с нужными параметрами
def test_no_matching_heroes():
    mock_data = json.dumps([
        {"name": "Hero1", "gender": "female", "height": 180, "work": False},
        {"name": "Hero2", "gender": "female", "height": 170, "work": True},
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_tallest_hero_from_file("male", True, "dummy_path")
    
    assert result is None

# Тест 3: Проверка работы, если несколько героев имеют одинаковую высоту
def test_multiple_same_height_heroes():
    mock_data = json.dumps([
        {"name": "Hero1", "gender": "male", "height": 180, "work": True},
        {"name": "Hero2", "gender": "male", "height": 180, "work": True},
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_tallest_hero_from_file("male", True, "dummy_path")
    
    assert result["height"] == 180
    assert result["name"] in ["Hero1", "Hero2"]

# Тест 4: Проверка работы, если список героев пуст
def test_empty_heroes_list():
    mock_data = json.dumps([])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_tallest_hero_from_file("male", True, "dummy_path")
    
    assert result is None

# Тест 5: Проверка работы с разным регистром в поле gender
def test_gender_case_insensitive():
    mock_data = json.dumps([
        {"name": "Hero1", "gender": "Male", "height": 190, "work": True},
        {"name": "Hero2", "gender": "male", "height": 185, "work": True},
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_tallest_hero_from_file("male", True, "dummy_path")
    
    assert result["name"] == "Hero1"
    assert result["height"] == 190

# Тест 6: Проверка работы с героями, у которых поле height не является числом
def test_invalid_height_value():
    mock_data = json.dumps([
        {"name": "Hero1", "gender": "male", "height": "invalid", "work": True},
        {"name": "Hero2", "gender": "male", "height": 185, "work": True},
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(TypeError):
            get_tallest_hero_from_file("male", True, "dummy_path")
