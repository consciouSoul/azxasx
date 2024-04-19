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


app = Client("saveFiles", api_id=config.APP_ID, api_hash=config.API_HASH)


async def main():
    data = {}
    downloadedMessageIDs = mongodb.find_one({"_id": 1})["messageIDs"]
    async with app:
        async for message in app.get_chat_history(config.NEW_CHANNEL_ID):
            message: Message
            if not message.document or message.video:
                continue

            mid = (
                int(message.document.file_name.split(".")[0])
                if message.document
                else int(message.video.file_name.split(".")[0])
            )
            if mid not in downloadedMessageIDs:
                print(f"Skipped {mid}")
                continue

            caption = message.caption.split("\n")[0] if message.caption else ""
            data[mid] = caption
            print(f"Saved {mid} - {len(data)}")

            with open("filenames.json", "w", encoding="utf8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
