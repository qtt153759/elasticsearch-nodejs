from datetime import date
from facebook_scraper import get_posts
import json
from pathlib import Path
import sys

today = date.today()
print("Today's date:", today)
listposts=[]
facebook_url="https://m.facebook.com/"
with open("./url/"+str(today)+"/870665749718859.json") as fp:
    url_list = json.load(fp)
id_list=[]
print(len(url_list))

for i in range(int(sys.argv[1]),int(sys.argv[2])):
    id_list.append(url_list[i]["post_id"])
print(id_list)

posts = get_posts(post_urls=[facebook_url+str(id) for id in id_list],cookies='cockies.json', options={"comments":True})


Path("./data_post/"+str(today)).mkdir(parents=True, exist_ok=True)

   
with open("./data_post/"+str(today)+"/870665749718859_"+sys.argv[1]+"_"+sys.argv[2]+".json", 'a+') as f:
  f.write("[")
  posts=list(posts)
  for i in range(len(posts)-1):
      try:
        posts[i]["comments_full"]="".join(posts[i]["comments_full"])
        del posts[i]["original_text"]
      except KeyError as ex:
          print("No such key: '%s'" % ex)
      json.dump(posts[i], f, ensure_ascii=False, default=str)
      f.write(",\n")
  json.dump(posts[len(posts)-1], f, ensure_ascii=False, default=str)
  f.write("]")