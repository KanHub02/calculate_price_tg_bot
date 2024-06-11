from decouple import config
import aiohttp

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


# Fetch categories from API
async def get_catalog_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/catalog/api/v1/get-category-list/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []

# Fetch products from API
async def get_catalog_products(category_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/catalog/api/v1/get-category-retrieve/{category_id}/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []