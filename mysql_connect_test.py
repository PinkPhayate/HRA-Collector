# -*- coding: utf-8 -*-
import MySQLdb
import re
import json

conn = MySQLdb.connect(
    host="localhost",
    db="hra",
    user="root",
    port=3306
)
cursor = conn.cursor()
conn.set_character_set('utf8mb4')
cursor.execute('SET NAMES utf8mb4;')
cursor.execute('SET CHARACTER SET utf8mb4;')
cursor.execute('SET character_set_connection=utf8mb4;')

hid, jocker = '2011105000', '川田将雅'
rid = '201309040605'
# args = (hid, jocker,)
# sql = ("""SELECT * FROM history where race_id = %s""" % rid)
# cursor.execute(sql)
# res = cursor.fetchall()
# print res

try:
    # cursor.execute("""SELECT * FROM history where horse_id = %s and jocker = %s"""% (hid, jocker))
    cursor.execute("SELECT * FROM history where horse_id = %s and race_id = %s", (hid, rid))
    # cursor.execute("""SELECT * FROM history where horse_id = %s and race_id = %s""" , (hid, rid))
    res = cursor.fetchall()
    # TODO  二件以上ある場合はどうなるの
    print ('response: ' + res)
except:
    print('cannot execute query')
