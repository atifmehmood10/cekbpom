import pyodbc

conn = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                      'Server=localhost;'
                      'Database=master;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('')
for row in cursor:
    print(row)