import aiohttp
from decouple import config

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")

async def get_partner_lead_info():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/manager/api/v1/get-partnerlead-info/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []
