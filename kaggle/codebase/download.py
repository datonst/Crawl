import os
from sqlite3 import connect

def get_one_dataset(command, compe_id, name):
    os.system(command)
    old_name = f"{command[32:]}.zip"    
    identity = str(compe_id) + "_" + name
    new_name = f"kaggle_dataset/{identity}"
    os.rename(old_name, new_name)
    update_value_in_db(compe_id, new_name)

def update_value_in_db(compe_id, new_path):
    with connect(
        "kaggle"
    ) as conn:
        cursor = conn.cursor()
        
        stmt = f"""
        UPDATE competitions
        SET dataset_path = '{new_path}'
        WHERE id = {compe_id}
        """
        cursor.execute(stmt)

        conn.commit()
