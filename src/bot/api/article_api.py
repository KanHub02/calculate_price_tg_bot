import aiohttp
from decouple import config

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


# Fetch articles from API
async def get_article_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_ADDRESS}/article/api/v1/article-list/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


# Fetch article details from API
async def get_article_detail(article_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_ADDRESS}/article/api/v1/article-detail/{article_id}/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


# Fetch other list from API
async def get_rest_other_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BACKEND_ADDRESS}/article/api/v1/other-list/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []
