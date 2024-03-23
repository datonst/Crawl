import sqlite3
import pandas as pd

conn = sqlite3.connect("../kaggle") 

COMPE_QUERY = '''SELECT id,name,download_command,dataset_path FROM competitions'''
SOL_QUERY = '''SELECT * FROM solutions'''
QUERY_TABLE_INFO = 'PRAGMA table_info(competitions)'

FULL_RETRIEVE_QUERY = '''
    SELECT c.*, s.link FROM competitions c JOIN solutions s ON c.id = s.competition_id GROUP BY c.id
'''

UPDATE_QUERY = '''
    UPDATE competitions SET name = "TEST" WHERE id = ?"
'''



def main():
    df = pd.read_sql_query(FULL_RETRIEVE_QUERY, conn)
    df.to_csv("kaggle.csv", index=False)
    

if __name__ == "__main__":
    main()


