import requests
import pathlib
import os
import csv
import time
api_key1= "?api_key=1bcf4a758acbdd85dafa511a54f667a2"
api_key2= "?api_key=76381cef2064df94a4afdeafe624abfa"
tasks_url_json=[]
tasks_url_xml=[]
dir = pathlib.Path().resolve();
dir = dir.joinpath("remote");
dir = dir.joinpath("openml");
newdir_task = dir.joinpath("tasks") 
newdir_data= dir.joinpath("datasets") 
if not os.path.exists(newdir_task):
    os.makedirs(newdir_task)
if not os.path.exists(newdir_data):
    os.makedirs(newdir_data)

datas_url=[]
datalist_url =[]
list_id=[]
lk=[]












              # Làm việc với json
def download_lk(url):
        with requests.get(url) as response:
            try :
                val = response.json()
                task_id = val['task']['task_id']
                data_set_id = val['task']['input'][0]['data_set']['data_set_id']
                # filename = newdir_task.joinpath(str(task_id+".json"))
                lk.append([task_id,data_set_id])
                # with open(filename, mode="w") as file:
                #     file.write(json.dumps(val))
            except:
                print("not found taks json")
                return
                
def download_task(url,task_id):
        with requests.get(url) as response:
            try :
                filename = newdir_task.joinpath(str(task_id)+".xml")
                with open(filename, 'wb') as file:
                        file.write(response.content)
            except:
                print("not found tasks xml")
                return










def download_url(url,data_id):
            try :
                with requests.get(url) as response:
                    val =  response.json()
                    data_url=val["data_set_description"]["url"]
                    data_url = data_url + api_key1
                    datas_url.append(data_url)
                    list_id.append(data_id)
                    return [data_url,data_id]
            except:
                print("not found url " + str(data_id))
                return[]    
        




def download_data(url,data_id):
            try :
                with requests.get(url,stream=True) as response:
                    filename = newdir_data.joinpath(str(data_id)+".arff")
                    with open(filename, mode="wb") as file:
                            file.write(response.content)
            except:
                print("Not found data " + str(data_id))
                # for chunk in response.iter_content(chunk_size=10 * 1024):
                #     file.write(chunk)
            




# for url in datas_url:
#     # response = requests.get(url) #, stream=True
#     with requests.get(url, stream=True) as response:
        # if "content-disposition" in response.headers:
        #     header = response.headers["content-disposition"]
        #     filename = header.split("filename=")[1]
        # else:
        #     filename = url.split("/")[-1]
        # with open(filename, mode="wb") as file:
        #     for chunk in response.iter_content(chunk_size=10 * 1024):
        #         file.write(chunk)


# for id in range(1306,361346):  #361346
#     url = f"https://www.openml.org/api/v1/xml/task/{id}"
#     tasks_url_xml.append(url)
#     download_task(url,id)
#     time.sleep(2)
# print("DONE 1-----------------------------------------")
for data_id in range(2006,45675): #45675
    api_key1,api_key2 =api_key2,api_key1 
    url = f"https://www.openml.org/api/v1/json/data/{data_id}" +api_key1
    datalist_url.append(url)
    val = download_url(url,data_id)

    if(val) :
         download_data(val[0],val[1])

print("DONE 2---------------------------------------")

# for id in range(1,361346):  #361346
#     url = f"https://www.openml.org/api/v1/json/task/{id}"
#     tasks_url_json.append(url)
#     download_lk(url)
#     time.sleep(2)
# print("DONE 3---------------------------------------")


# rc=0
# for da in datas_url:
#      download_data(url,list_id[rc])
#      time.sleep(2)
#      rc+=1






with open(dir.joinpath('banglienket.csv'), mode='w') as csv_file:
    csv_file.write('tasks_id,data_id')
    csv_file.write('\n')
    for s in lk:
        csv_file.write(str(s[0]) +"," + str(s[1]))
        csv_file.write('\n')
        print(s[0] + " . " + s[1])