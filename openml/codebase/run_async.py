import requests,aiohttp,asyncio
import pathlib
import os,json
import aiofiles
import csv
api_key1= "?api_key=1bcf4a758acbdd85dafa511a54f667a2"
api_key2= "?api_key=76381cef2064df94a4afdeafe624abfa"

tasks_url_json=[]
dir = pathlib.Path().resolve();
dir = dir.joinpath("remote");
dir = dir.joinpath("openml");
newdir_task = dir.joinpath("tasks") 
newdir_data= dir.joinpath("datasets") 
if not os.path.exists(newdir_task):
    os.makedirs(newdir_task)
if not os.path.exists(newdir_data):
    os.makedirs(newdir_data)
plus = 0
datas_url=[]
datalist_url =[]
list_id=[]
lk=[]
tasks_url_xml=[]
# for id in range(1 + plus,45675): #45675
    
#     temp= api_key1 
#     api_key1 =api_key2
#     api_key2=temp

#     url = f"https://www.openml.org/api/v1/json/data/{id}" + api_key1
#     datalist_url.append(url)


# for id in range(1,361346):  #361346
#     temp= api_key1 
#     api_key1 =api_key2
#     api_key2=temp
#     url = f"https://www.openml.org/api/v1/json/task/{id}" + api_key1 
#     tasks_url_json.append(url)
    

# for id in range(1,361346):  #361346
#     temp= api_key1 
#     api_key1 =api_key2
#     api_key2=temp
#     url = f"https://www.openml.org/api/v1/xml/task/{id}" + api_key1
#     tasks_url_xml.append(url)


list_id_task=[]
t = dir.joinpath("banglienket.csv")
with open(t) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    check=True

    for row in csv_reader:
        temp= api_key1 
        api_key1 =api_key2
        api_key2=temp
        list_id_task.append(row[0])
        url = f"https://www.openml.org/api/v1/xml/task/{row[0]}" 
        tasks_url_xml.append(url)
print("SUCCESS")


async def download_url_data(url,data_id,session):
    try :
            async with session.get(url) as response:
                global api_key1,api_key2
                temp=api_key1 
                api_key1 = api_key2
                api_key2=temp
                val = await response.json()
                data_url=val["data_set_description"]["url"] 
                data_url = data_url + api_key1
                datas_url.append(data_url)
    except:
        print("not found url " + str(data_id))
        return
    list_id.append(data_id)







              # Làm việc với json
async def download_lk(url,session):
        async with session.get(url,allow_redirects=False,timeout=200000) as response:
            try :
                val = await response.json()
                task_id = val['task']['task_id']
                data_set_id = val['task']['input'][0]['data_set']['data_set_id']
                lk.append([task_id,data_set_id])
            except:
                print("not found" )
                return


         #download_by_xml       
async def download_task(url,task_id,session):
    await asyncio.sleep(2)
    async with aiohttp.ClientSession() as session:
        async with session.get(url,allow_redirects=False,timeout=200000) as response:
            try :
                filename = newdir_task.joinpath(str(task_id)+".xml")
                with open(filename, mode="wb") as file:
                    while True:
                        chunk = await response.content.read()
                        if not chunk:
                            break
                        file.write(chunk)
                
            except:
                print("not found")
                return

async def main_task():
    tasks=[]
    data_id =0 + plus
    # async with aiohttp.ClientSession() as session:
        # for url in datalist_url:
        #     data_id+=1
        #     task = asyncio.create_task(download_url_data(url,data_id,session))
        #     tasks.append(task)
    
    timeout = aiohttp.ClientTimeout(total=200000)
    connector = aiohttp.TCPConnector(limit=40)
    dummy_jar = aiohttp.DummyCookieJar()
    i =0
    async with aiohttp.ClientSession(connector=connector, timeout=timeout, cookie_jar=dummy_jar) as session:
        for url in tasks_url_xml:
            file = newdir_task.joinpath(str(list_id_task[i])+".xml")
            if not os.path.exists(file):
                # print(file)
                task = asyncio.ensure_future(download_task(url,list_id_task[i],session))
                tasks.append(task)
            i+=1
        # for url in tasks_url_json:
        #     task = asyncio.ensure_future(download_lk(url,session))
        #     tasks.append(task)
        await asyncio.gather(*tasks)



asyncio.run(main_task())











async def download_data(url,data_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try :
                    filename = newdir_data.joinpath(str(data_id)+".arff")
                    with open(filename, mode="wb") as file:
                        while True:
                            chunk = await response.content.read()
                            if not chunk:
                                break
                            file.write(chunk)
                except:
                    print("Not found data " +str(data_id))



async def main_data():
    tasks=[]
    id =0
    for url in datas_url:
        file = newdir_data.joinpath(str(list_id[id])+".arff")
        if not os.path.exists(file):
            print(file)
            task = asyncio.create_task(download_data(url,list_id[id]))
            tasks.append(task)
        id+=1
    await asyncio.gather(*tasks)
print("RUn")


# with open(dir.joinpath('link_data.csv'), mode='w') as csv_file:
#     id =0
#     for s in datas_url:
#         csv_file.write(str(s) +" " + str(list_id[id]))
#         csv_file.write('\n')
#         id+=1

# asyncio.run(main_data())




# with open(dir.joinpath('banglienket.csv'), mode='w') as csv_file:
#     csv_file.write("tasks_id,data_id")
#     csv_file.write("\n")
#     for s in lk:
#         csv_file.write(str(s[0]) +"," + str(s[1]))
#         csv_file.write("\n")
