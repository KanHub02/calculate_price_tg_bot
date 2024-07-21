from decouple import config
import aiohttp

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


async def create_tg_user(data):
    url = f"{BACKEND_ADDRESS}/client/api/v1/create-telegram-user/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"

async def get_manager_ids():
    url = f"{BACKEND_ADDRESS}/manager/api/v1/get-manager-ids"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []
            
async def get_manager_card_list():
    url = f"{BACKEND_ADDRESS}/manager/api/v1/get-manager-card-list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []
