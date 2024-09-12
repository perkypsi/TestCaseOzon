# TestCaseOzon

Скрипт позволяет получить самого высокого героя по полу и занятости. Апи используется только для получения файла с данными по всем героям, на основе которого работает функция get_tallest_hero_from_file.

Основная функция находится в app.py.

get_data.py асинхронно подключается по API(http://superheroapi.com/api/) после чего сохраняет все данные в файл json.

Сигнатура функции: `def get_tallest_hero_from_file(gender, has_work, filepath) -> Union[dict, None]`

Тесты расположены в файле tests.py

Python 3.12.6
Необходимые зависимости в файле requirements.txt