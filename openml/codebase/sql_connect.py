from sqlite3 import connect, Error
from getpass import getpass
import pathlib
import csv,os 
import pandas as pd

competition_list = []
solution_list = []
dir = pathlib.Path().resolve();
dir = dir.joinpath("remote");
dir = dir.joinpath("openml");
newdir_task = dir.joinpath("tasks") 
newdir_data= dir.joinpath("datasets") 
datasets_list=[]
tasks_list=[]
#-------------------------------
#convert csv file into set of data
for id in range(1,45675): #45675
    data=newdir_task.joinpath(str(id) +".arff")
    if os.path.exists(newdir_task):
        datasets_list.append([str(id),str(data)])
    
check = set()
# with open(dir.joinpath("codebase").joinpath('banglienket.csv'), mode='r',encoding="Windows-1252") as f:
#     reader = csv.reader(f) 
#     flag = False #There no need to add column title (first column)
#     for row in reader:
#         if flag: 
#             if row[0] in check:
#                 print("Have contain")
#             task_id = row[0]

#             data_id= row[1]
#             check.add(task_id)
#             task=newdir_task.joinpath(str(task_id) +".xml")
#             if os.path.exists(newdir_task):
#                 tasks_list.append([str(task_id),str(task),str(data_id)])
#             # competition_list.append((name, overview, description, 
#             #                          evaluation, data_description, download_command,
#             #                          html_data_path, html_overview_path))
            
#             #-------------------------------------------------------
#         else: flag = True


#selenium\venv\styles\1.Open Problems – Single-Cell Perturbations\data.html

#------------------------
db_path = "/home/thieuluu/automl_dataset/openml/openml"
with connect(
    db_path
) as conn:
    data_insert_query = """
    INSERT INTO datasets
    (data_id,data_path)
    VALUES (?, ?)
    """

    task_insert_query = """
    INSERT INTO tasks
    (task_id, task_path, data_id)
    VALUES (?, ?,?)
    """

    remove_query = """
    DELETE FROM datasets
    """

    drop_tasks_query = """
    DROP TABLE tasks
    """

    drop_datasets_query = """
    DROP TABLE datasets
    """

    create_datasets_query = """
    CREATE TABLE datasets (data_id varchar(50) PRIMARY KEY, data_path varchar(15550));
    """
    
    create_tasks_query = """
    CREATE TABLE tasks (task_id varchar(50) PRIMARY KEY, task_path varchar(15550),
    data_id varchar(50) CONSTRAINT data_to_task REFERENCES datasets (data_id) ON DELETE NO ACTION ON UPDATE NO ACTION);
    """

    show_tasks="""SELECT * FROM tasks;"""
    show_datasets="""SELECT * FROM datasets;"""

    show_test="""SELECT u1.task_path,u2.data_path FROM tasks AS u1
                INNER JOIN datasets AS u2 ON u1.data_id = u2.data_id;"""
    cursor = conn.cursor()
    # cursor.execute(create_datasets_query)
    # cursor.execute(create_tasks_query)
    # cursor.executemany(data_insert_query, datasets_list)
    # cursor.executemany(task_insert_query, tasks_list)
    # cursor.execute(drop_datasets_query)
    lists = conn.execute(show_test)

    conn.commit() 

for row in lists:
    print(row)