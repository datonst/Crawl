from bs4 import BeautifulSoup

import sqlite3
import os
from download import get_one_dataset, update_value_in_db

data_source = []
command = []
id_list = []
name_list = []
def get_path_and_command():
    conn = sqlite3.connect("kaggle")
    query = '''SELECT HTML_data_source_path, download_command, id, name FROM competitions'''
    cursor = conn.cursor()

    #---------------------------
    res = cursor.execute(query)
    for src in res:
        data_source.append(src[0])
        command.append(src[1])  
        id_list.append(src[2])
        name_list.append(src[3])

    #--------------------------
    conn.close()

#---- only download file which has size <= 5GB -------
def get_possible_download_command():
    possible_compo = []
    for i in range(0,len(data_source)):
        src = data_source[i]
        try:
            with open(src,'r') as f:
                html_plain_text = f.read()
                soup = BeautifulSoup(html_plain_text, 'html.parser')
                elements = soup.find_all('p', class_='sc-dKfzgJ sc-hIqOWS jQQULV dclpAt')
                try:
                    volume = elements[2].text
                except IndexError:
                    continue
                unit = volume[len(volume)-2:]

                try:
                    cap = float(volume[:len(volume)-3])
                except ValueError:
                    possible_compo.append((id_list[i],command[i],name_list[i]))
                if unit == 'GB' and cap > 5: 
                    continue
                else:
                    possible_compo.append((id_list[i],command[i],name_list[i]))
        except FileNotFoundError:
            print("not found")
    return possible_compo

if __name__ == '__main__':
    get_path_and_command()
    
    possible_compo = get_possible_download_command()
    cur = 0
    
    #due to server down occuring, i will redownload from file 296, which correspond to index 178 in possible_compo 
    RESTART_INDEX = 178
    for compo in possible_compo:
        # print(compo[0], compo[1])
        
        name = compo[2]
        compe_id = compo[0]
        command = compo[1]

        if cur >= RESTART_INDEX:
            try:
                get_one_dataset(command, compe_id, name)
            except Exception:
                with open("fail_command.txt", 'a') as f:
                    f.write(command + "\n")

        # print(cur, compe_id) 
        cur += 1


