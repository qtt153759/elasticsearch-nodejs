from datetime import date
import json
import os
from pathlib import Path

today = date.today()
today="2023-02-01"
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


# Path(sink_path).mkdir(parents=True, exist_ok=True)
os.system("sudo mkdir -p "+sink_path) 
os.system("sudo touch "+sink_path+today+".json")


with open(sink_path+today+".json",'w+') as sinkfile:
    file=''
    for source_file in res:
      with open(source_path+source_file) as fp:
          file+=fp.read()
    sinkfile.write(file)

