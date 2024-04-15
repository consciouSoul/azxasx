import os
import time
import json
import time
import config
import logging
import asyncio


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
            print(message)
            if video:
                print(f"Downloading {message.id}")
                
                with open(f"files/info/{message.id}.json", "w", encoding='utf8') as f:
                    json.dump(json.loads(str(message)), f, ensure_ascii=False, indent=3)
                
                await app.download_media(message, file_name=f"files/{message.id}.mp4")
                await asyncio.sleep(1)
                
                # send the file to admin's chat
                await app.send_document(config.ADMIN_CHAT_ID, f"files/{message.id}.mp4")
                await app.send_document(config.ADMIN_CHAT_ID, f"files/info/{message.id}.json")
                os.remove(f"files/{message.id}")
            
            
            print(message.id)


app.run(main())
