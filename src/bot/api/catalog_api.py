from decouple import config
import aiohttp

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


# Fetch categories from API
async def get_catalog_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_ADDRESS}/catalog/categories/") as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


# Fetch subcategories from API
async def get_subcategory_list(category_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_ADDRESS}/catalog/categories/{category_id}/subcategories/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


# Fetch products from API
async def get_catalog_products(category_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_ADDRESS}/catalog/categories/{category_id}/products/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []
