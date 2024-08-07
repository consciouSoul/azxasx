import time
import httpx

from database import Database
from datetime import datetime, timezone

from config import links


ses = httpx.Client(timeout=30, follow_redirects=True)
db = Database("mongodb+srv://Nusab19:0092100921@firstcluster.eh81nbz.mongodb.net/?retryWrites=true&w=majority&appName=FirstCluster", db_name="url-monitor")


def check(url):
    monitored = {
        "url": url,
        "status": None,
        "response_time": None,
        "time": datetime.now(timezone.utc)
    }
    try:
        start = time.time()
        response = ses.get(url)
        end = time.time()
        monitored["status"] = response.status_code
        monitored["response_time"] = (end - start) * 1000
    except Exception as e:
        monitored["status"] = 500
        monitored["response_time"] = (time.time() - start) * 1000
        monitored["error"] = str(e)
    
    monitored["done_at"] = datetime.now(timezone.utc)

    return monitored


for i in range(10):
    for link in links:
        if not link.startswith("http"):
            continue

        data = check(link)
        last_data = db.findOne("data", {"url": link})
        if last_data:
            del last_data["_id"]
            del last_data["url"]
        
        data["last_data"] = last_data

        db.update("data", {"url": link}, data)
        print(i+1, data)

        time.sleep(0.5)

    time.sleep(5)
