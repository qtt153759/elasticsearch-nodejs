from datetime import date
import json
import os
from pathlib import Path
import random
from time import sleep

import requests
from facebook_scraper import get_posts

groupIds:'list[str]'
groupIds=['352230071875035','1523459548029885',"224105692857136","1457408924575160","174764463261090","3237453733026579","870665749718859"]

def getGroupIdbyDay()->'list[str]':
    today = date.today()
    return [groupIds[today.weekday]]
def getCookies()->str:
    x=random.uniform(0,1)
    if (x>0.5):
        return '/home/airflow/data_facebook/cockies.json'
    return '/home/airflow/data_facebook/cockies.json'
def crawl_url():
    sink_path="/home/airflow/data_facebook/data_url/"
    today = date.today()
    today = "2023-02-11"
    print("Step 1 Today's date:", today)
    groupIdsByDay=getGroupIdbyDay()
    for groupId in groupIdsByDay:
        # for post in posts:
        Path(sink_path+str(today)).mkdir(parents=True, exist_ok=True)
        # get url
        with open(sink_path+str(today)+"/"+groupId+".json", 'w+') as f:
            posts = get_posts(group=groupId,cookies=getCookies(),options={"allow_extra_requests":False})
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
        sleep(60*random.uniform(1,2))

def crawl_post():
    today = date.today()
    today = "2023-02-11"
    print("Step 2 Today's date:", today)
    source_path = "/home/airflow/data_facebook/data_url/"+str(today)+"/"
    sink_path="/home/airflow/data_facebook/data_post/"+str(today)+"/"
    facebook_url="https://m.facebook.com/"
    Path(sink_path).mkdir(parents=True, exist_ok=True)
    isExist = os.path.exists(sink_path)
    print("exist:",isExist)
    groupIdsByDay=getGroupIdbyDay()
    for groupId in groupIdsByDay:
        with open(source_path+groupId) as fp:
            url_list = json.load(fp)
        print(len(url_list))
        

        id_list=[]
        for i in range(len(url_list)):
            id_list.append(url_list[i]["post_id"])
        chunks = [id_list[x:x+20] for x in range(0, len(id_list), 20)]
        print(chunks)
        for i in range(len(chunks)):
            with open(sink_path+str(i)+"_"+groupId, 'a+') as f:
                posts = get_posts(post_urls=[facebook_url+str(id) for id in chunks[i]],cookies=getCookies(), options={"comments":True})
                f.write("[")
                posts=list(posts)
                for j in range(len(posts)-1):
                    posts[j]["comments_full"]="".join(posts[j]["comments_full"])
                    try:
                        del posts[j]["original_text"]
                    except KeyError as ex:
                        print("No such key: '%s'" % ex)
                    json.dump(posts[j], f, ensure_ascii=False, default=str)
                    f.write(",\n")
                json.dump(posts[len(posts)-1], f, ensure_ascii=False, default=str)
                f.write("]")    
            sleep(60*random.uniform(1,2))
        sleep(60*random.uniform(3,4))

                    

def create_bulk_data():
    today = date.today()
    today = "2023-02-11"
    # folder path
    source_path = "/home/airflow/data_facebook/data_post/"+today+"/"
    sink_path="/home/airflow/data_facebook/data_final/"

    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(source_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(source_path, path)):
            res.append(path)
    print(res)

    Path(sink_path).mkdir(parents=True, exist_ok=True)

    with open(sink_path+today+".json",'a+') as file:
        for source_file in res:
            print(source_file)
            with open(source_path+source_file) as fp:
                    datas = json.load(fp)

            
            for data in datas:
                for ignore_type in ["original_text","original_request_url","likes","post_text"]:
                    try:
                      del data[ignore_type]
                    except KeyError as ex:
                      print("No such key: '%s'" % ex)
                data["time"]=data["time"].replace(" ","T")
                # file.write("{\"create\":{\"_id\":"+str(data['post_id'])+"}}")
                # file.write("\n")
                json.dump(data, file, ensure_ascii=False, default=str)
                file.write("\n")

def indexElasticsearch():
    today = date.today()
    today ="2023-02-11"
    # folder path
    source_path="/home/airflow/data_facebook/data_final/"+str(today)+".json"
    isExists=os.path.isfile(source_path)
    response=""
    print(os.environ['WEB_HOSTS']+"/fbScraper?date="+str(today))
    if isExists:
        # sleep(60)
        response=requests.get(os.environ['WEB_HOSTS']+"/fbScraper?date="+str(today))
    else:
        response="source_path not exist"
    print(response)
