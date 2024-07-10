from decouple import config
import aiohttp

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


async def fetch_cargo_types():
    url = f"{BACKEND_ADDRESS}/logistic/api/v1/get-cargo-types/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_packaging_types():
    url = f"{BACKEND_ADDRESS}/logistic/api/v1/get-cargo-packages/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def create_logistic_request(data):
    url = f"{BACKEND_ADDRESS}/client/api/v1/create-logistic-request/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"
