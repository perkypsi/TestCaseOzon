import json

def get_tallest_hero_from_file(gender, has_work, filepath):
    with open(filepath, 'r') as json_file:
        heroes = json.load(json_file)

    filtered_heroes = [
        hero for hero in heroes
        if hero['gender'].lower() == gender.lower() and
           (hero['work'] == has_work)
    ]

    tallest_hero = max(
        filtered_heroes,
        key=lambda hero: hero['height'],
        default=None
    )

    return tallest_hero
