# from sqlalchemy import create_engine, text
# import pandas as pd
# from datetime import datetime



# # Konfigurasi koneksi ke database
# db_user = 'root'
# db_password = ''
# db_host = '127.0.0.1:3306'
# db_name = 'bpsproject_db'

# # Membuat koneksi ke database

# connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
# engine = create_engine(connection_string)

# # Membaca file CSV
# csv_file_path = '../data/sample_ubah.csv'
# data = pd.read_csv(csv_file_path)
# data.insert(loc=4, column="verif", value=1)
# data['created_at'] = datetime.now()
# data['updated_at'] = datetime.now()
# # data.to_csv('../data/sample_ubah.csv', index=False)


# # Fungsi untuk memeriksa apakah data sudah ada dalam tabel
# def data_exists(judul, connection):
#     result = connection.execute(text("SELECT 1 FROM berita WHERE headline = :judul"), {"judul": judul})
#     return result.fetchone() is not None


# # with engine.connect() as connection:
# #     judul = data['headline'][0]  # Assuming you want to check the first headline in your CSV
# #     if data_exists(judul, connection):
# #         print('Data sudah ada')
# #     else:
# #         print('data belum ada')

# def insert_data_to_db(dataframe, engine):
#     with engine.connect() as connection:
#         for index, row in dataframe.iterrows():
#             if not data_exists(row['headline'], connection):
#                 # print('data berhasil ditambahkan')
#                 sql = text("INSERT INTO berita (periode, label, headline, content, predik, verif, created_at, updated_at) VALUES (:periode, :label, :headline, :content, :predik, :verif, :created_at, :updated_at)")
                # connection.execute(sql, {
                #     'periode': row['periode'], 
                #     'label': row['label'], 
                #     'headline': row['headline'], 
                #     'content': row['content'], 
                #     'predik': row['predik'], 
                #     'verif': row['verif'], 
                #     'created_at': row['created_at'], 
                #     'updated_at': row['updated_at']
                # })
#             else:
#                 print('data tidak ditambahkan')

# # Fungsi untuk memasukkan data ke tabel Berita
# # def insert_data_to_db(dataframe, table_name, engine):
# #     dataframe.to_sql(table_name, con=engine, if_exists='append', index=False)

# # Memasukkan data ke tabel Berita
# insert_data_to_db(data, engine)


# from sqlalchemy import create_engine, text
# import pandas as pd
# from datetime import datetime
# from sqlalchemy.exc import IntegrityError

# # Konfigurasi koneksi ke database
# db_user = 'root'
# db_password = ''
# db_host = '127.0.0.1:3306'
# db_name = 'bpsproject_db'

# # Membuat koneksi ke database
# connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
# engine = create_engine(connection_string)

# # Membaca file CSV
# csv_file_path = '../data/data_test.csv'
# data = pd.read_csv(csv_file_path)
# # data.insert(loc=4, column="verif", value=1)
# data['created_at'] = datetime.now()
# data['updated_at'] = datetime.now()

# # Fungsi untuk memeriksa apakah data sudah ada dalam tabel
# def data_exists(judul, connection):
#     result = connection.execute(text("SELECT 1 FROM testing WHERE judul = :judul"), {"judul": judul})
#     return result.fetchone() is not None

# def insert_data_to_db(dataframe, engine):
#     with engine.connect() as connection:
#         for index, row in dataframe.iterrows():
#             print(f"Checking existence for judul: {row['judul']}")  # Debug statement
#             if not data_exists(row['judul'], connection):
#                 print(f"Inserting judul: {row['judul']}")  # Debug statement
#                 sql = text("INSERT INTO testing (periode, judul, category, sentimen, created_at, updated_at) VALUES (:periode, :judul, :category, :sentimen, :created_at, :updated_at)")
#                 try:
#                     connection.execute(sql, {
#                         'periode': row['periode'], 
#                         'judul': row['judul'], 
#                         'category': row['category'], 
#                         'sentimen': row['sentimen'], 
#                         'created_at': row['created_at'], 
#                         'updated_at': row['updated_at']
#                     })
#                     print(f"Inserted judul: {row['judul']}")  # Debug statement
#                 except IntegrityError as e:
#                     print(f'IntegrityError for judul {row["judul"]}: {e}')  # Debug statement
#             else:
#                 print(f'judul already exists: {row["judul"]}')  # Debug statement

# # Memasukkan data ke tabel Berita
# insert_data_to_db(data, engine)


from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
print(data.head())  # Debug statement
data['created_at'] = datetime.now()
data['updated_at'] = datetime.now()

# Fungsi untuk memeriksa apakah data sudah ada dalam tabel
def data_exists(judul, connection):
    result = connection.execute(text("SELECT 1 FROM testing WHERE judul = :judul"), {"judul": judul})
    exists = result.fetchone() is not None
    print(f"Data exists for judul {judul}: {exists}")  # Debug statement
    return exists

def insert_data_to_db(dataframe, engine):
    with engine.begin() as connection:
        for index, row in dataframe.iterrows():
            print(f"Checking existence for judul: {row['judul']}")  # Debug statement
            if not data_exists(row['judul'], connection):
                print(f"Inserting judul: {row['judul']}")  # Debug statement
                sql = text("INSERT INTO testing (periode, judul, category, sentimen, created_at, updated_at) VALUES (:periode, :judul, :category, :sentimen, :created_at, :updated_at)")
                try:
                    connection.execute(sql, {
                        'periode': row['periode'], 
                        'judul': row['judul'], 
                        'category': row['category'], 
                        'sentimen': row['sentimen'], 
                        'created_at': row['created_at'], 
                        'updated_at': row['updated_at']
                    })
                    print(f"Inserted judul: {row['judul']}")  # Debug statement
                except IntegrityError as e:
                    print(f'IntegrityError for judul {row["judul"]}: {e}')  # Debug statement
                except Exception as e:
                    print(f'Error inserting data for judul {row["judul"]}: {e}')  # Debug statement
            else:
                print(f'judul already exists: {row["judul"]}')  # Debug statement

# Memasukkan data ke tabel Berita
try:
    with engine.connect() as connection:
        print("Connected to the database successfully")  # Debug statement
        insert_data_to_db(data, engine)
except Exception as e:
    print(f"Failed to connect to the database: {e}")  # Debug statement
