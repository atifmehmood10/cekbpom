import os

from flask import Flask, render_template
from flask_mysqldb import MySQL

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'cekbpom'
    mysql = MySQL(app)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        data = []
        try:
            cursor = mysql.connection.cursor()
            select_data = "select Produk, Nama_Produk,Merk,Pendaftar, Diterbitkan_Oleh from cekbpom.companieshouse;"
            cursor.execute(select_data)
            data = cursor.fetchall()
            print(data)
        except Exception:
            print("Exception")
        return render_template('index.html', data=data)
    return app

