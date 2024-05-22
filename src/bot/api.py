from decouple import config
import aiohttp


async def create_tg_user(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-telegram-user/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"


async def fetch_cargo_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-cargo-types/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_packaging_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-ff-packages/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


async def fetch_packaging_sizes(packaging_id):
    url = (
        f"http://127.0.0.1:8080/fulfillment/api/v1/get-ff-package-sizes/{packaging_id}/"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data["sizes"]  # Получаем только массив размеров
            else:
                return []


async def create_tg_user(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-telegram-user/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"


async def fetch_cargo_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-cargo-types/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_packaging_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-cargo-packages/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_marking_types():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-ff-marks/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return []


async def fetch_packaging_options():
    url = "http://127.0.0.1:8080/fulfillment/api/v1/get-ff-packages/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []


async def create_logistic_request(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-logistic-request/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"


async def create_fulfillment_request(data):
    url = "http://127.0.0.1:8080/client/api/v1/create-fulfillment-request/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                response_data = await response.json()
                return f"Error: {response_data.get('detail', 'Unknown error')}"


async def fetch_warehouses():
    url = "http://127.0.0.1:8080/stock/api/v1/get-stock-list/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []
