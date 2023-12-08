import unittest
import sqlite3

from sql import SQL

import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from googleSheet import GoogleSheet 

sql=SQL('My_money_test.sql','users')
gs=GoogleSheet('creds_4.json')

conn=sqlite3.connect('My_money_test.sql')
cur=conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id varchar(50), pass varchar(50), link varchar(150), infForBot varchar(150), link2 varchar(150))')
cur.execute('SELECT * FROM users WHERE id=="22222"')
results=cur.fetchall()
if not(results):
    cur.execute('INSERT INTO users (id,pass,link,infForBot,link2) VALUES("11111","password1","http//:test11","1/1/1/1/1/1","http//:test12")')
    cur.execute('INSERT INTO users (id,pass,link,infForBot,link2) VALUES("22222","password2","http//:test21","2/2/2/2/2/2","http//:test22")')
conn.commit()
cur.close()
conn.close()

CREDENTIALS_FILE='creds_4.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheetId='1sEiRzbjab1v5BZG2cTQ01teYGt7tPtb8eec-Nu8CMY4'

service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {"valueInputOption": "USER_ENTERED","data": [{"range": "Лист номер один!A1:B2","majorDimension": "ROWS","values":[['A1','B1'],['A2','B2']]}]}).execute()

class sglSelectTest(unittest.TestCase):
    def test_1(self):
        self.assertEqual(sql.select('pass','id',"11111")[0][0], 'password1')

    def test_2(self):
        self.assertEqual(sql.select('pass','id','22222')[0][0], 'password2')

    def test_3(self):
        self.assertEqual(sql.select('link','id','11111')[0][0], 'http//:test11')

    def test_4(self):
        self.assertEqual(sql.select('link','id','22222')[0][0], 'http//:test21')

    def test_5(self):
        self.assertEqual(sql.select('infForBot','id','11111')[0][0], '1/1/1/1/1/1')

    def test_6(self):
        self.assertEqual(sql.select('infForBot','id','22222')[0][0], '2/2/2/2/2/2')

    def test_7(self):
        self.assertEqual(sql.select('link2','id','11111')[0][0], 'http//:test12')

    def test_8(self):
        self.assertEqual(sql.select('link2','id','22222')[0][0], 'http//:test22')
class sglInsertTest(unittest.TestCase):
    def test_1(self):
        sql.insert('id',"'%s'"%('33333'))
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT id FROM users WHERE id=="33333"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="33333"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0][0], '33333')

    def test_2(self):
        sql.insert('id,pass',"'%s','%s'"%('33333','password3'))
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT pass FROM users WHERE id=="33333"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="33333"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0][0], 'password3')

    def test_3(self):
        sql.insert('id,pass,link',"'%s','%s','%s'"%('33333','password3','http//:test31'))
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT pass,link FROM users WHERE id=="33333"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="33333"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0], ('password3','http//:test31'))

    def test_4(self):
        sql.insert('id,pass,link,infForBot',"'%s','%s','%s','%s'"%('33333','password3','http//:test31','3/3/3/3/3/3'))
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT pass,infForBot FROM users WHERE id=="33333"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="33333"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0], ('password3','3/3/3/3/3/3'))

    def test_5(self):
        sql.insert('id,pass,link,infForBot,link2',"'%s','%s','%s','%s','%s'"%('33333','password3','http//:test31','3/3/3/3/3/3','http//:test32'))
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT * FROM users WHERE id=="33333"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="33333"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0], ('33333','password3','http//:test31','3/3/3/3/3/3','http//:test32'))

class sglUpdateTest(unittest.TestCase):
    def test_1(self):
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('INSERT INTO users (id,pass,link,infForBot,link2) VALUES("44444","password4","http//:test41","4/4/4/4/4/4","http//:test42")')
        conn.commit()
        cur.close()
        conn.close()
        sql.update('id','55555','id','44444')
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT id FROM users WHERE id=="55555"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="55555"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0][0], '55555')

    def test_2(self):
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('INSERT INTO users (id,pass,link,infForBot,link2) VALUES("44444","password4","http//:test41","4/4/4/4/4/4","http//:test42")')
        conn.commit()
        cur.close()
        conn.close()
        sql.update('pass',"'password5'",'id','44444')
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT pass FROM users WHERE id=="44444"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="44444"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0][0], 'password5')

    def test_3(self):
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('INSERT INTO users (id,pass) VALUES("44444","password4")')
        conn.commit()
        cur.close()
        conn.close()
        sql.update('link2',"'http//:test52'",'id','44444')
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT link2 FROM users WHERE id=="44444"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="44444"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0][0], 'http//:test52')

    def test_2(self):
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('INSERT INTO users (id,pass,link,infForBot,link2) VALUES("44444","password4","http//:test41","4/4/4/4/4/4","http//:test42")')
        conn.commit()
        cur.close()
        conn.close()
        sql.update('pass',"'password5'",'id','44444')
        sql.update('link',"'http//:test51'",'id','44444')
        sql.update('infForBot',"'5/5/5/5/5/5'",'id','44444')
        sql.update('link2',"'http//:test52'",'id','44444')
        conn=sqlite3.connect('My_money_test.sql')
        cur=conn.cursor()
        cur.execute('SELECT * FROM users WHERE id=="44444"')
        results=cur.fetchall()
        cur.execute('DELETE FROM users WHERE id=="44444"')
        conn.commit()
        cur.close()
        conn.close()
        self.assertEqual(results[0], ('44444','password5','http//:test51','5/5/5/5/5/5','http//:test52'))

class gsGetData(unittest.TestCase):
    def test_1(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!A1").get('values',[])[0][0], 'A1')

    def test_2(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!A2").get('values',[])[0][0], 'A2')

    def test_3(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!B1").get('values',[])[0][0], 'B1')

    def test_4(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!B2").get('values',[])[0][0], 'B2')

    def test_5(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!A1:B2").get('values',[]), [['A1','B1'],['A2','B2']])
    
    def test_6(self):
        self.assertEqual(gs.getData(spreadsheetId,"Лист номер один!B3"), 'No data found.')

class gsUpdateData(unittest.TestCase):
    def test_1(self):
        gs.updateData(spreadsheetId,"Лист номер один!A1:B2",[['1','2'],['3','4']])
        self.assertEqual(service.spreadsheets().values().get(spreadsheetId = spreadsheetId,range="Лист номер один!A1:B2").execute().get('values',[])[0][0], '1')

    def test_2(self):
        gs.updateData(spreadsheetId,"Лист номер один!A1:B2",[['1','2'],['a','4']])
        self.assertEqual(service.spreadsheets().values().get(spreadsheetId = spreadsheetId,range="Лист номер один!A1:B2").execute().get('values',[])[1][0], 'a')

    def test_3(self):
        gs.updateData(spreadsheetId,"Лист номер один!A1:B2",[['a','22'],['ann','4']])
        self.assertEqual(service.spreadsheets().values().get(spreadsheetId = spreadsheetId,range="Лист номер один!A1:B2").execute().get('values',[]),[['a','22'],['ann','4']])
        
if __name__ == "__main__":
    unittest.main()
