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
parents_phone_num_data = sdb_system.search_phone_num_parents()[0]
send_data = sdb_system.search_phone_num_parents()[1]



print(len(send_data))

@app.route('/parents_message')
def parents_send_message():
    for i in range(len(send_data)):
        parents_message = f'안녕하세요! {student_name_data[i]} 학부모님 수다방학원입니다. \n금일 수업 내용입니다. \n[진도] : {send_data[i][2]} \n[과제] : {send_data[i][3]} \n[과제 수행도] : {send_data[i][4]} \n[벌점] : {send_data[i][5]} \n[테스트] : {send_data[i][6]} \n[반평균] : {send_data[i][8]} \n[최고점] : {send_data[i][9]} \n[특이사항] : {send_data[i][10]}'
        '''
        data = {
            'messages': [
                {
                    'to': parents_phone_num_data[i],
                    'from': SEND.SENDNUMBER,
                    'subject': '수다방학원',
                    'text': parents_message
                }
            ]
        }
        
        res = message.send_many(data)
        print(f"{student_name_data[i]} 학부모에게 성공적으로 전송했습니다")
        print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
        '''
    return "전송하였습니다."

@app.route('/student_message')
def student_send_message():
    for i in range(len(send_data)):
        student_message = f'안녕! 수다방이야 {student_name_data[i]} 반가워! \n[진도] : {send_data[i][2]} \n[과제] : {send_data[i][3]} \n[과제 수행도] : {send_data[i][4]} \n[벌점] : {send_data[i][5]} \n[테스트] : {send_data[i][6]} \n[반평균] : {send_data[i][8]} \n[최고점] : {send_data[i][9]} \n[특이사항] : {send_data[i][10]}'
        '''
        data = {
            'messages': [
                {
                    'to': student_phone_num_data[i],
                    'from': SEND.SENDNUMBER,
                    'subject': '수다방학원',
                    'text': student_message
                }
            ]
        }
        
        res = message.send_many(data)
        print(f"{student_name_data[i]}에게 성공적으로 전송했습니다")
        print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))
        '''
    return "전송하였습니다."
        
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)