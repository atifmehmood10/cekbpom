import json
import logging
from datetime import datetime

import mysql.connector

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               database="cekbpom")
mycursor = mydb.cursor()

def readJson(file_path):

    f = open(file_path)
    data = json.load(f)
    sql = "INSERT into companieshouse (Nomor_Registrasi, Tanggal_Terbit, Diterbitkan_Oleh, Produk, " \
          "Nama_Produk, Merk, Kemasan, Pendaftar) " \
          "VALUES(%s, %s, %s, %s ,%s, %s, %s, %s)"
    for items in data:
        date = items['Tanggal_Terbit']
        date = datetime.strptime(date, '%d-%m-%Y').date()
        values = (items['Nomor_Registrasi'],
                  date,
                  items['Diterbitkan_Oleh'],
                  items['Produk'],
                  items['Nama_Produk'],
                  items['Merk'],
                  items['Kemasan'],
                  items['Pendaftar'])
        try:
            mycursor.execute(sql, values)
        except mysql.connector.errors.IntegrityError:
            print("Duplicate")
    mydb.commit()




