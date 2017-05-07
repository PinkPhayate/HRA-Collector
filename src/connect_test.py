import MySQLdb

def showUser():

    connector = MySQLdb.connect(
            user='root',
            passwd='',
            host='localhost',
            charset='utf-8',
            db='HRA')

    cursor = connector.cursor()
    cursor.execute("show columns from Horse")

    for row in cursor.fetchall():
        print(row)

    cursor.close
    connector.close

if __name__ == "__main__":
    showUser()
