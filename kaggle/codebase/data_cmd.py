#Func: download dataset from command
#TODO: download, avoid file more than 5GB


import os

START_INDEX = 0
END_INDEX = 100

def get_data_download_command():
    data_download_command = []
    with open("command.txt","r") as f:
        for line in f:
            data_download_command.append(line)
    return data_download_command
        
        
