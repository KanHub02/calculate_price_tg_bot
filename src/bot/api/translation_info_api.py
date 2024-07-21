import aiohttp
from decouple import config

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

async def get_crypto_info():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/course/api/v1/get-crypto-info/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


async def get_rf_info():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/course/api/v1/get-rf-info/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []