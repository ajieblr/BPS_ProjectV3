from app import app
from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine, text

# Konfigurasi koneksi ke database
db_user = 'root'
db_password = ''
db_host = '127.0.0.1:3306'
db_name = 'bpsproject_db'

# Membuat koneksi ke database
connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_string)


@app.route('/', methods=['GET', 'POST'])
def home():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM berita"))
        data = [dict(row._mapping) for row in result]
    return render_template('home.html', data=data)

# @app.route('/filter', methods=['GET'])
# def filter_data():
#     portal = request.args.get('portal', '')
    
#     query = "SELECT * FROM berita"
#     if portal:
#         query += f" WHERE label = :portal"
    
#     with engine.connect() as connection:
#         result = connection.execute(text(query), {'portal': portal})
#         data = [dict(row._mapping) for row in result]
    
#     return jsonify(data=data)

@app.route('/filter', methods=['GET'])
def filter_data():
    portal = request.args.get('portal', '')
    tahun = request.args.get('tahun', '')
    # triwulan = request.args.get('triwulan', '')
    kategori = request.args.get('kategori', '')

    query = "SELECT * FROM berita WHERE 1=1"
    params = {}
    
    if portal:
        query += " AND label = :portal"
        params['portal'] = portal
    if tahun:
        query += " AND YEAR(STR_TO_DATE(periode, '%m/%d/%Y')) = :tahun"
        params['tahun'] = tahun
    if kategori:
        query += " AND predik = :kategori"
        params['kategori'] = kategori

    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        data = [dict(row._mapping) for row in result]
    
    return jsonify(data=data)


@app.route('/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM berita WHERE id = :id"), {'id': news_id})
        news = result.fetchone()
        if news:
            news = dict(news._mapping)
        else:
            news = {}
    return jsonify(news)

@app.route('/predict')
def page1():
    return render_template('predict.html')

@app.route('/profile')
def page2():
    return render_template('profile.html')

