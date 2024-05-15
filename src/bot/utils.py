import aiohttp


async def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, data={"chat_id": chat_id, "text": text}
        ) as response:
            return await response.json()
