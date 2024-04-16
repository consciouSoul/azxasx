import os
import time
import json
import time
import config
import logging
import asyncio


from pyrogram import Client
from database import mongodb
from pyrogram.types import Message

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

os.system("rm -rf files")


app = Client("saveFiles", api_id=config.APP_ID, api_hash=config.API_HASH)

chatID = -1002048501622

if not os.path.exists("files"):
    os.makedirs("files/info")


async def main():
    count = mongodb.find_one({"_id": 1})["count"]
    start = time.time()
    async with app:
        async for message in app.get_chat_history(chatID):
            message: Message
            video = message.video
            if video:
                if message.id in mongodb.find_one({"_id": 1})["messageIDs"]:
                    print(f"Skipping {message.id}")
                    continue
            
                print(message)
                print(f"Downloading {message.id}")

                mongodb.update_one(
                    {"_id": 1}, {"$push": {"messageIDs": message.id}}, upsert=True
                )

                await app.download_media(message, file_name=f"files/{message.id}.mp4")
                await asyncio.sleep(1)

                # send the file to admin's chat
                await app.send_document(
                    config.ADMIN_CHAT_ID,
                    f"files/{message.id}.mp4",
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                )
                os.remove(f"files/{message.id}.mp4")
                count += 1
                print(f"Downloaded {count} files")
                mongodb.update_one({"_id": 1}, {"$inc": {"count": 1}}, upsert=True)
                if time.time() - start > 17 * 60:
                    print("Exiting...")
                    break

            print(message.id)


app.run(main())
