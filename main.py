import os
import time
import json
import time
import config
import logging
import asyncio


from pyrogram import Client
from database import mongodb
from datetime import datetime
from pyrogram.types import Message

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

os.system("rm -rf files")


app = Client("premium", api_id=config.APP_ID, api_hash=config.API_HASH)

chatID = -1002048501622

if not os.path.exists("files"):
    os.makedirs("files/info")


def convert_bytes(size):
    # Define the units and their respective suffixes
    units = ["B", "KB", "MB", "GB", "TB"]
    # Calculate the appropriate unit index based on the size
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    # Format the size with two decimal places and the appropriate unit
    return f"{size:.2f} {units[unit_index]}"


class Timer:
    current: int = 0
    startTime: int = 0


def downloadProgress(current: int, total: int):
    diff = time.time() - Timer.startTime
    percentage = (current * 100) / total
    downloaded = convert_bytes(current)
    totalSize = convert_bytes(total)
    speed = convert_bytes(current / diff)
    eta = round((total - current) / (current / diff))
    if time.time() - Timer.current < 1:  # update every 1 seconds
        return
    Timer.current = time.time()
    print(
        f"{percentage:.2f}% Downloaded {downloaded}/{totalSize} @{speed}/s ETA: {eta} seconds"
    )


def uploadProgress(current: int, total: int):
    diff = time.time() - Timer.startTime
    percentage = (current * 100) / total
    uploaded = convert_bytes(current)
    totalSize = convert_bytes(total)
    speed = convert_bytes(current / diff)
    eta = round((total - current) / (current / diff))

    if time.time() - Timer.current < 1:  # update every 1 seconds
        return
    Timer.current = time.time()
    print(
        f"{percentage:.2f}% Uploaded {uploaded}/{totalSize} @{speed}/s ETA: {eta} seconds"
    )


async def main():
    count = mongodb.find_one({"_id": 1})["count"]
    start = time.time()
    async with app:
        # start from the beginning
        async for message in app.get_chat_history(chatID):
            message: Message
            video = message.video
            if not video:
                print(f"Skipping {message.id}")
                continue

            if video:
                if message.id in mongodb.find_one({"_id": 1})["messageIDs"]:
                    print(f"Already have {message.id}")
                    continue

                print(f"Downloading {message.id}")
                Timer.startTime = time.time()
                await app.download_media(
                    message,
                    file_name=f"files/{message.id}.mp4",
                    progress=downloadProgress,
                )
                await asyncio.sleep(1)

                print(f"Uploading {message.id}")
                Timer.startTime = time.time()
                await app.send_document(
                    config.ADMIN_CHAT_ID,
                    f"files/{message.id}.mp4",
                    caption=message.caption,
                    caption_entities=message.caption_entities,
                    progress=uploadProgress,
                )
                count += 1
                os.remove(f"files/{message.id}.mp4")
                print(f"Downloaded {count} files")
                mongodb.update_one(
                    {"_id": 1}, {"$push": {"messageIDs": message.id}}, upsert=True
                )
                mongodb.update_one({"_id": 1}, {"$inc": {"count": 1}}, upsert=True)
                if time.time() - start > 23 * 60:
                    print("Exiting...")
                    break


app.run(main())
