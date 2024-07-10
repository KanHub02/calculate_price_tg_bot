import aiohttp
from decouple import config

BACKEND_ADDRESS = config("BACKEND_ADDRESS", "http://web:8811")


# Отправка отзыва на сервер
async def send_feedback(user_id, feedback):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_ADDRESS}/client/api/v1/create-feedback-usefull/",
            json={"telegram_client_id": user_id, "feedback": feedback},
        ) as response:
            return response.status == 200
