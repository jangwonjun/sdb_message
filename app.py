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
parents_phone_num_data = sdb_system.search_phone_num_parents()
send_data = sdb_system.send_student_message()

print(len(student_phone_num_data)) #sdb db에서 이름과 대조하여 동일한 학생을 찾은 경우
print(student_phone_num_data) #[학생전화번호,이름] 
print(len(send_data)) #실제로 메세지를 보내야하는 인원의 수(즉, 정리하자면 3번 리스트에 정리한 인원)


@app.route('/message_send')
def student_send_message():
    #여기서의 for문은 보내야할 인원이 아닌, 동일한 학생을 찾은 경우로 생각하고 진행해야지 올바름.
    for i in range(len(student_phone_num_data)):
        
        data = {
                'messages': [
                    {
                        'to': student_phone_num_data[i][0],
                        'from': SEND.SENDNUMBER,
                        'subject': '수다방학원',
                        'text': send_data[i][0]
                    }
                ]
            }
        res = message.send_many(data)
        print(f"{send_data[i][1]}에게 성공적으로 전송했습니다")
        print(json.dumps(json.loads(res.text), indent=2, ensure_ascii=False))

    return "전송하였습니다."

        
@app.route('/main')
def main():
    return render_template('index.html')

    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=FLASK_ENUM.PORT)