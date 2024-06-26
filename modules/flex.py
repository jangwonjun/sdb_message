import gspread
from oauth2client.service_account import ServiceAccountCredentials
from env import FLASK_ENUM,SQL
import pymysql
from flask import Flask, request, redirect, render_template, url_for, session

class login_system():
    def __init__(self):
        pass
    
    def new_login(self,id,password):
        self.id = id 
        self.password = password

        conn = pymysql.connect(
            host=SQL.HOST, port=SQL.PORT, user=SQL.ID, passwd=SQL.PASSWORD, db=SQL.DB_NAME, charset='utf8'
        )

        cursor = conn.cursor()

        id_sql = "SELECT * FROM users WHERE id = %s"
        cursor.execute(id_sql,(self.id))
        id_result = cursor.fetchall()
        

        conn.commit()
        conn.close()

        data = []
        
        print(id_result)
        if id_result[0][0] == id:
            print("pass")
            if id_result[0][1] == password:
                data.append((id_result[0][2],id_result[0][3]))
            else:
                status_code = "password_incorrect"
                print("아이디 혹은 비밀번호가 잘못되었습니다.")
            
        else:
            print("아이디 혹은 비밀번호가 잘못되었습니다.")

        return data
        
