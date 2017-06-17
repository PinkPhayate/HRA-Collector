import MySQLdb

def showUser():

    connector = MySQLdb.connect(
            user='root',
            passwd='root',
            port=3333,
            host='127.0.0.1',
            db='HRA')

    cursor = connector.cursor()
    cursor.execute("show columns from history")

    for row in cursor.fetchall():
        print(row)

    cursor.close
    connector.close

if __name__ == "__main__":
    showUser()
