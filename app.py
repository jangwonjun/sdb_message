import json
from src.lib import message, storage
import pandas
from env import SEND, FLASK_ENUM
from tqdm import tqdm
from modules.candidate import candidate_data
from flask import Flask, request, redirect, render_template, url_for, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__, static_url_path='/static')


sdb_system = candidate_data()

student_phone_num_data = sdb_system.search_phone_num_student()
num_inf = sdb_system.send_student_num()
send_data = sdb_system.send_student_message()

print('최종적으로 전송할 데이터',student_phone_num_data)

@app.route('/message_send', methods=['POST'])
def student_send_message():
    success_data_student = []
    success_data_parents = []
    print("도달에 성공하였습니다.")
    print("학생/학부모 문자 전송준비완료...")

    for i in range(len(student_phone_num_data)):

        
        data = {
                'messages': [
                    {
                        'to': student_phone_num_data[i][0],
                        'from': SEND.SENDNUMBER,
                        'subject': '수다방학원',
                        'text': student_phone_num_data[i][3]
                    }   
                ]
            }
        res = message.send_many(data)
        
        print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
        print(f"{student_phone_num_data[i][2]}에게 성공적으로 전송했습니다")
        success_data_student.append([student_phone_num_data[i][2],student_phone_num_data[i][0]])

        data2 = {
                'messages': [
                    {
                        'to': student_phone_num_data[i][1],
                        'from': SEND.SENDNUMBER,
                        'subject': '수다방학원',
                        'text': student_phone_num_data[i][3]
                    }
                ]
            }
        res = message.send_many(data2)
        print(f"{student_phone_num_data[i][2]} 학부모에게 성공적으로 전송했습니다")
        print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
        success_data_parents.append([{student_phone_num_data[i][2]},student_phone_num_data[i][1]])
        

    return render_template('message.html', send_result_student=success_data_student, send_result_parent=success_data_parents,target_data=send_data)
        
@app.route('/main')
def main():
    return render_template('index.html')

    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)