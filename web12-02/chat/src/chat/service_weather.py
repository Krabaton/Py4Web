import aiohttp
import asyncio
from src.settings import config


async def get_weather(city):
    params = {'q': city, 'appid': config["common"]["appid"], 'units': 'metric'}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.openweathermap.org/data/2.5/weather', params=params) as response:
            result = await response.json()
            if response.status == 200:
                return f"У місті {city} температура зараз {result['main']['temp']}"
            else:
                return f"При спробі взнати температуру у місті {city}, була отримана помилка {result['message']}"


async def main():
    city = 'Poltava'
    result = await get_weather(city)
    print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())