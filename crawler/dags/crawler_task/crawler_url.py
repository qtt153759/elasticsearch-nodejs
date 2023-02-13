from datetime import date
import random
import sys
import time
from anyio import sleep
from facebook_scraper import get_posts
import json
from pathlib import Path

def crawl_url():
    today = date.today()
    print("Today's date:", today)
    groupIds=['174764463261090','3237453733026579','224105692857136','1457408924575160']
    for groupId in groupIds:
        sleep(60*random.uniform(1,2))
        posts = get_posts(group=groupId,cookies='cockies.json',options={"allow_extra_requests":False})
        # for post in posts:
        Path("./url/"+str(today)).mkdir(parents=True, exist_ok=True)
        # get url
        with open("./url/"+str(today)+"/"+groupId+".json", 'a') as f:
            posts=list(posts)
            if len(posts)==0:
                print("empty post")
                exit(0)

            f.write("[")
            for i in range(len(posts)-1):
                try:
                    del posts[i]["original_text"]
                except KeyError as ex:
                    print("No such key: '%s'" % ex)
                # f.write(str(posts[i]).replace("\"","\\\"").replace(r"\U","\\").replace("'","\"")+",")
                json.dump(posts[i], f, ensure_ascii=False, default=str)
                f.write(",\n")
            json.dump(posts[len(posts)-1], f, ensure_ascii=False, default=str)
            f.write("]")

if __name__ == "__main__":
    groupId = sys.argv
    crawl_url(groupId[1])