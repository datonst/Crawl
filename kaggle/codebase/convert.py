from sqlite3 import connect, Error

import csv  

def get_competition_and_solution_list():
    competition_list = []
    solution_list = []
    #-------------------------------
    #convert csv file into set of data
    with open("data.csv", 'r', encoding="Windows-1252") as f:
        reader = csv.reader(f) 
        flag = False #There no need to add column title (first column)
        for row in reader:
            if flag:  

                #-----------INFORMATIONS SPACE-----------------------------
                compe_id = row[0]
                name, overview, description = row[1], row[2], row[3]
                evaluation, data_description, download_command = row[4], row[5], row[6]
                html_data_path = f"../html/{compe_id}.{name}/data.html"
                html_overview_path = f"../html/{compe_id}.{name}/overview.html"

                #-----------APPENDING INTO COMPETITION LIST-----------------------------
                competition_list.append((name,
                                        overview,
                                        description, 
                                        evaluation,
                                        data_description,
                                        download_command,
                                        html_data_path,
                                        html_overview_path))
                
                #-------------------------------------------------------
                
                all_link = row[7] 
                
                all_link = all_link.split("\n",4) #max 5 link so just split 4 times
                for link in all_link:
                    solution_list.append((compe_id, link))

            else: 
                flag = True
    return competition_list, solution_list

#------------------------
def main():
    competition_list, solution_list = get_competition_and_solution_list()

    '''
    Table structure

+----+-----------------------------+----------------------------------+----------------------------------+-----------+---------------------+---------------------+--------------------------+-----------------------------
| id |            name             |            overview              |           description            | evaluation|  data_description  | download_command    | HTML_data_source_path    | HTML_overview_source_path  |
+----+-----------------------------+----------------------------------+----------------------------------+-----------+---------------------+---------------------+--------------------------+-----------------------------+
|    |                             |                                  |                                  |           |                     |                     |                          |                             |                             
+----+-----------------------------+----------------------------------+----------------------------------+-----------+---------------------+---------------------+--------------------------+-----------------------------+

    Or you can use sql query: PRAGMA table_info(table_name)  
    example: PRAGMA table_info(competitions)
    '''
    with connect(
        "kaggle"
    ) as conn:
        compe_insert_cmd = """
        INSERT INTO competitions
        (name,overview,description,evaluation,data_description,download_command,HTML_data_source_path,HTML_overview_source_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        sol_insert_cmd = """
        INSERT INTO solutions
        (competition_id, link)
        VALUES (?, ?)
        """

        drop_solution_cmd = """
        DROP TABLE solutions
        """

        drop_competition_cmd = """
        DROP TABLE competitions
        """

        create_competition_cmd = """
        CREATE TABLE competitions (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, overview TEXT, 
        description TEXT, evaluation TEXT, data_description TEXT, download_command TEXT, 
        HTML_data_source_path TEXT, HTML_overview_source_path TEXT, dataset_path TEXT);
        """
        
        create_solution_cmd = """
        CREATE TABLE solutions (id INTEGER PRIMARY KEY AUTOINCREMENT, 
        competition_id INTEGER CONSTRAINT sol_of_compe REFERENCES competitions (id) ON DELETE NO ACTION ON UPDATE NO ACTION, 
        link TEXT);
        """
        update_solution_cmd = """
        UPDATE solutions
        SET link = replace(link, '\n', '')
        WHERE link LIKE '%\n'
        """
        cursor = conn.cursor()
        
        cursor.execute(update_solution_cmd)
        '''
        SQL commands go here
        Everything must be commit 
        '''
        # cursor.executemany(sol_insert_cmd, solution_list)

        conn.commit()

if __name__ == '__main__':
    main()
