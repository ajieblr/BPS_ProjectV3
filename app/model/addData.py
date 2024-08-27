import pymysql
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime



# Konfigurasi koneksi ke database
db_user = 'root'
db_password = ''
db_host = '127.0.0.1:3306'
db_name = 'bpsproject_db'

# Membuat koneksi ke database

connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_string)

# Membaca file CSV
csv_file_path = '../data/data_test.csv'
data = pd.read_csv(csv_file_path)
data['created_at'] = datetime.now()
data['updated_at'] = datetime.now()
# print(data['created_at'])

# Fungsi untuk memeriksa apakah data sudah ada dalam tabel
def data_exists(judul, connection):
    result = connection.execute("SELECT 1 FROM testing WHERE judul = %s", (judul,))
    return result.fetchone() is not None


def insert_data_to_db(dataframe, table_name, engine):
    with engine.connect() as connection:
        for index, row in dataframe.iterrows():
            if not data_exists(row['judul'], connection):
                connection.execute(
                    f"INSERT INTO {table_name} (periode, judul, category, sentimen, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)",
                    (row['periode'], row['judul'], row['category'], row['sentimen'], row['created_at'], row['updated_at'])
                )

# Fungsi untuk memasukkan data ke tabel Berita
# def insert_data_to_db(dataframe, table_name, engine):
#     dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)

# Memasukkan data ke tabel Berita
insert_data_to_db(data, 'testing', engine)
