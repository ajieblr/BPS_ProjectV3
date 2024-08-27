
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from datetime import datetime as dt, timedelta

# Konfigurasi koneksi ke database
db_user = 'root'
db_password = ''
db_host = '127.0.0.1:3306'
db_name = 'bpsproject_db'

# Membuat koneksi ke database
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_string)

yesterday = dt.now() - timedelta(days=1)
start_date = yesterday
end_date = yesterday

# Membaca file CSV
csv_file_path = f'../model_handler/hasil_predik/Predict_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
data = pd.read_csv(csv_file_path)
# data.insert(loc=4,column="predik", value='None')
data['created_at'] = datetime.now()
data['updated_at'] = datetime.now()

# Fungsi untuk memeriksa apakah data sudah ada dalam tabel
def data_exists(judul, connection):
    result = connection.execute(text("SELECT 1 FROM berita WHERE headline = :headline"), {"headline": judul})
    exists = result.fetchone() is not None
    print(f"Data exists for judul {judul}: {exists}")  # Debug statement
    return exists

def insert_data_to_db(dataframe, engine):
    with engine.begin() as connection:
        for index, row in dataframe.iterrows():
            print(f"Checking existence for judul: {row['headline']}")  # Debug statement
            if not data_exists(row['headline'], connection):
                print(f"Inserting headline: {row['headline']}")  # Debug statement
                sql = text("INSERT INTO berita (periode, label, headline, content, predik, created_at, updated_at, sentimen, link) VALUES (:periode, :label, :headline, :content, :predik, :created_at, :updated_at, :sentimen, :link)")
                try:
                    connection.execute(sql, {
                    'periode': row['periode'], 
                    'label': row['label'], 
                    'headline': row['headline'], 
                    'content': row['content'], 
                    'predik': row['predik'],
                    'created_at': row['created_at'], 
                    'updated_at': row['updated_at'],
                    'sentimen': row['sentimen'],
                    'link': row['link']
                })
                    print(f"Inserted judul: {row['headline']}")  # Debug statement
                except IntegrityError as e:
                    print(f'IntegrityError for judul {row["headline"]}: {e}')  # Debug statement
                except Exception as e:
                    print(f'Error inserting data for judul {row["headline"]}: {e}')  # Debug statement
            else:
                print(f'judul already exists: {row["headline"]}')  # Debug statement

# Memasukkan data ke tabel Berita
try:
    with engine.connect() as connection:
        print("Connected to the database successfully")  # Debug statement
        insert_data_to_db(data, engine)
except Exception as e:
    print(f"Failed to connect to the database: {e}")  # Debug statement