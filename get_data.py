import json
import aiohttp
import asyncio
import os
from config import ACCESS_TOKEN, FILEPATH, MAX_ID, AMOUNT_ASYNC_CALL_API

async def get_heroes_info(session, hero_id, semaphore):
    async with semaphore:
        try:
            url = f"http://superheroapi.com/api/{ACCESS_TOKEN}/{hero_id}/"
            async with session.get(url) as response:
                return await response.json()
        except Exception as e:
            print(f"Ошибка при запросе данных героя с ID {hero_id}: {e}")

async def fetch_and_save_heroes(filepath='data.json'):
    max_id = MAX_ID
    semaphore = asyncio.Semaphore(AMOUNT_ASYNC_CALL_API)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for hero_id in range(1, max_id + 1):
            tasks.append(get_heroes_info(session, hero_id, semaphore=semaphore))

        heroes_data = await asyncio.gather(*tasks)
    
    heroes = []
    for data in heroes_data:
        if len(data['appearance']['height']) == 2:
            if 'meters' in data['appearance']['height'][1]:
                height = float(data['appearance']['height'][1].replace(' meters', '')) * 100
            elif 'cm' in data['appearance']['height'][1]:
                height = float(data['appearance']['height'][1].replace(' cm', ''))
            else:
                height = 0
                print(data['appearance']['height'][1])
        else:
            if 'Shaker' in data['appearance']['height'][0]:
                height = 50
            else:
                height = 0
                print('len = 1')
                print(data['appearance']['height'][1])
        
        heroes.append(
                {
                    "name": data['name'],
                    "height": height,
                    'gender': data['appearance']['gender'],
                    'work': True if data['work']['base'] != "-" else False
                }
        )

    with open(filepath, 'w') as json_file:
        json.dump(heroes, json_file)

async def get_data():
    filepath = FILEPATH

    if not os.path.exists(filepath):
        print("Данные о героях не найдены. Загружаем данные из API...")
        await fetch_and_save_heroes(filepath)
    else:
        print("Данные уже загружены")

asyncio.run(get_data())