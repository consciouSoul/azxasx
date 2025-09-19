import os
from dotenv import load_dotenv

load_dotenv()

MongoURI = os.environ.get("MongoURI")

links = """
https://mdc-7cbt.onrender.com/
https://report-league.onrender.com/

https://contest-hive.vercel.app/api/all
https://toph-api.onrender.com/status
https://quranapi.pages.dev/api/1.json
https://nusab19.pages.dev/
""".split()

