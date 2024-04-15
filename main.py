import os
import time
import json
import time
import config
import logging
import asyncio
import pyrogram.methods


from pyrogram import Client
from pyrogram.types import Message


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Client("saveFiles", api_id=config.APP_ID, api_hash=config.API_HASH)

chatID = -1002048501622

if not os.path.exists("files"):
    os.makedirs("files/info")


async def main():
    async with app:
        async for message in app.get_chat_history(chatID):
            message: Message
            video = message.video
            if video:
                print(f"Downloading {message.id}")
                await app.download_media(message, file_name=f"files/{message.id}")
                with open(f"files/info/{message.id}.json", "w", encoding='utf8') as f:
                    json.dump(video.to_dict(), f, ensure_ascii=False, indent=3)
                await asyncio.sleep(1)
            
            print(message.id)


app.run(main())
