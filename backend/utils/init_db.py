import os
import sys
import duckdb
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import hash_password
from generated_csv import create_csv_from_json

os.makedirs(os.path.join(os.getcwd(), 'database'), exist_ok=True)

database_path = os.path.join(os.path.dirname(__file__), os.getcwd() + '/database/annotated_ultrasound.duckdb')
connection_database = duckdb.connect(database_path)

images_csv_path, segmentations_csv_path = create_csv_from_json()

dataframe_images = pd.read_csv(images_csv_path)
dataframe_segmentations = pd.read_csv(segmentations_csv_path)

connection_database.register('images_dataframe', dataframe_images)
connection_database.register('segmentations_dataframe', dataframe_segmentations)

connection_database.execute("""
    DROP TABLE IF EXISTS t_image;
    CREATE TABLE t_image AS
    SELECT * FROM images_dataframe
""")
connection_database.execute("""
    DROP TABLE IF EXISTS t_segmentation;
    CREATE TABLE t_segmentation AS
    SELECT * FROM segmentations_dataframe
""")
connection_database.execute("""
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT)
""")

hashed = hash_password("administrator")

connection_database.execute("INSERT INTO users VALUES (?, ?)", ("admin", hashed))

connection_database.commit()
print("La base a bien été initialisée avec utilisateur admin / administrator")

connection_database.close()