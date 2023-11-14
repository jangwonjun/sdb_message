import json
from src.lib import message, storage
import pandas
from env import SEND, FLASK_ENUM
from tqdm import tqdm
from modules.candidate import candidate_data
from flask import Flask, request, redirect, render_template, url_for, session

app = Flask(__name__, static_url_path='/static')

sdb_system = candidate_data()

student_phone_num_data = sdb_system.search_phone_num_student()[0]
student_name_data = sdb_system.search_phone_num_student()[1]
parents_phone_data = sdb_system.search_phone_num_parents()[0]
send_data = sdb_system.search_phone_num_parents()[1]

class_message = f'안녕! 수다방이야 {student_name_data[0]} 반가워! \n[진도] : {send_data[0][2]} \n[과제] : {send_data[0][3]} \n[과제 수행도] : {send_data[0][4]} \n[벌점] : {send_data[0][5]} \n[테스트] : {send_data[0][6]} \n[반평균] : {send_data[0][8]} \n[최고점] : {send_data[0][9]} \n[특이사항] : {send_data[0][10]}'



@app.route('/send_message')
def send_message():
    
    data = {
        'messages': [
            {
                'to': student_phone_num_data[0],
                'from': SEND.SENDNUMBER,
                'subject': 'TEST',
                'text': class_message
             }
         ]
       }
    
    res = message.send_many(data)
    print(f"{student_name_data[0]}에게 성공적으로 전송했습니다")
    print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
    return "전송하였습니다."
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)