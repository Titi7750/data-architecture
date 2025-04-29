import os
import shutil
import datetime

def backup_duckdb(source_path, backup_dir):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f'duckdb_backup_{now}.duckdb')

    if not os.path.exists(backup_dir):
        os.makedirs(os.path.join(os.getcwd(), 'saved_duckdb'), exist_ok=True)

    shutil.copy2(source_path, backup_path)
    print(f"Backup effectué : {backup_path}")

backup_duckdb('annotated_ultrasound.duckdb', os.getcwd() + '/saved_duckdb')
